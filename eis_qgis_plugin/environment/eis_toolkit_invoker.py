import json
import logging
import os
import queue
import subprocess
import threading
import time
from typing import Dict, List, TextIO, Tuple

from qgis.core import QgsProcessingFeedback, QgsProject, QgsRasterLayer

from eis_qgis_plugin.environment.eis_environment_handler import DockerEnvironmentHandler, VenvEnvironmentHandler
from eis_qgis_plugin.utils.message_manager import EISMessageManager
from eis_qgis_plugin.utils.settings_manager import EISSettingsManager

DEBUG = True
REQUIRED_EIS_TOOLKIT_VERSION = "1.0.3"

logger = logging.getLogger(__name__)


class TerminationException(Exception):
    """Exception error class raised if process is terminated by user."""


class EISToolkitInvoker:
    """Class that handles communication between EIS QGIS plugin and EIS Toolkit."""

    PROGRESS_PREFIX = "Progress:"
    OUT_RASTERS_PREFIX = "Output rasters:"
    RESULTS_PREFIX = "Results:"

    def __init__(self, env_type = None, venv_directory = None, docker_path = None, docker_image_name = None):
        """Initializes the EISToolkitInvoker."""
        env_type = EISSettingsManager.get_environment_selection() if env_type is None else env_type

        # Environment handler is needed for environment-specific communication
        if env_type == "venv":
            self.environment_handler = VenvEnvironmentHandler(
                EISSettingsManager.get_venv_directory() if venv_directory is None else venv_directory
            )
        elif env_type == "docker":
            self.environment_handler = DockerEnvironmentHandler(
                EISSettingsManager.get_docker_path() if docker_path is None else docker_path,
                EISSettingsManager.get_docker_image_name() if docker_image_name is None else docker_image_name,
                EISSettingsManager.get_docker_host_folder(),
                EISSettingsManager.get_docker_temp_folder()
            )
        else:
            raise ValueError(f"Unsupported environment type: {env_type}")

        self.python_free_environment = {key: value for key, value in os.environ.items() if not key.startswith("PYTHON")}
        self.cmd = []
        self.process = None


    @staticmethod
    def _format_algorithm_name(alg_name: str) -> str:
        """Formats the algorithm name for CLI use."""
        return (alg_name + "_cli").replace("_", "-")


    @staticmethod
    def _update_progress(stdout: str, feedback: QgsProcessingFeedback):
        """Updates the QGIS processing algorithm's progress based on the stdout message."""
        index = stdout.find("%")
        if index == -1:
            return
        progress = stdout[index-3:index].strip()
        # progress = stdout.split()[-1][:-1].strip()
        feedback.setProgress(int(progress))
        feedback.pushInfo(f"Progress: {progress}%")


    def _update_results(self, stdout: str, results: dict, feedback: QgsProcessingFeedback):
        """Prints the result information parsed from the stdout message."""
        json_str = stdout.split(self.RESULTS_PREFIX)[-1].strip()
        # Convert all found quotation marks to ensure succesfull deserialization.
        # NOTE that intended single quotation marks will get replaced too (but currently these
        # result messages should not have need for those)
        json_str = json_str.replace("\'", "\"")
        output_dict = json.loads(json_str)

        feedback.pushInfo("\n*** Results ***")
        feedback.pushInfo("-----------------------")
        for key, value in output_dict.items():
            feedback.pushInfo(f"* {key}: {value}")
        feedback.pushInfo("-----------------------\n ")

        results.update(output_dict)


    def _update_out_rasters(self, stdout: str):
        """
        Updates the QGIS project with output rasters parsed from the stdout message.

        Called *only* when processing algorithm has multiple rasters outputs. Single outputs
        are handled automatically.
        """
        # Extract the JSON part
        json_str = stdout.split(self.OUT_RASTERS_PREFIX)[-1].strip()

        # Deserialize the JSON-formatted string to a Python dict
        output_dict = json.loads(json_str)

        for name, path in output_dict.items():
            # TODO: Handle potential errors
            output_raster_layer = QgsRasterLayer(path, name)
            QgsProject.instance().addMapLayer(output_raster_layer)


    def assemble_cli_command(self, alg_name: str, typer_args: List[str], typer_options: List[str]):
        """
        Assembles command-line interface command for a specific algorithm of EIS toolkit.

        Args:
            alg_name: Name of the algorithm (in QGIS) to be invoked.
            typer_args: List of arguments for the Typer CLI.
            typer_options: List of options for the Typer CLI.
        """
        formatted_alg_name = self._format_algorithm_name(alg_name)
        self.cmd = self.environment_handler.assemble_cli_cmd(formatted_alg_name, typer_args, typer_options)
        
        if DEBUG:
            print(f"Assembled command: {self.cmd}")
            logging.debug("Assembled CLI command: %s", self.cmd)


    def verify_environment(self) -> Tuple[bool, str]:
        """Checks if the selected environment is valid."""
        return self.environment_handler.verify_environment()


    def verify_toolkit(self) -> Tuple[bool, str]:
        """Checks if EIS Toolkit can be found in the selected environment."""
        return self.environment_handler.verify_toolkit(REQUIRED_EIS_TOOLKIT_VERSION, self.python_free_environment)

    
    def upgrade_toolkit(self) -> Tuple[bool, str]:
        return self.environment_handler.upgrade_toolkit(self.python_free_environment)
    

    def run_toolkit_command(self, feedback: QgsProcessingFeedback) -> Dict:
        """Runs the toolkit command and captures the output."""
        if not self.cmd:
            EISMessageManager().show_message("Assemble a CLI call before trying to run EIS Toolkit.", "error")
            return

        results = {}
        q = queue.Queue()

        def enqueue_output(pipe: TextIO, queue: queue.Queue, process_event: threading.Event) -> None:
            for line in iter(pipe.readline, ''):
                if process_event.is_set():
                    break
                queue.put(line)
            pipe.close()

        # Execute EIS Toolkit through subprocess
        try:
            # QGIS sets some PYTHON environment variables that might disturb the external python the process is using
            logger.debug(f'Running command "{" ".join(self.cmd)}" with environment: {self.python_free_environment=}')

            creationflags = 0
            if os.name == 'nt':  # If Windows, prevent process window creation
                creationflags = subprocess.CREATE_NO_WINDOW

            self.process = subprocess.Popen(
                self.cmd,   
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                env=self.python_free_environment,
                creationflags=creationflags
            )

            process_event = threading.Event()

            stdout_thread = threading.Thread(target=enqueue_output, args=(self.process.stdout, q, process_event))
            stderr_thread = threading.Thread(target=enqueue_output, args=(self.process.stderr, q, process_event))

            stdout_thread.start()
            stderr_thread.start()

            while self.process.poll() is None:
                if feedback.isCanceled():
                    self.process.terminate()
                    self.process.wait()
                    process_event.set()
                    stdout_thread.join()
                    stderr_thread.join()
                    raise TerminationException("Execution cancelled.")

                try:
                    line = q.get_nowait()
                except queue.Empty:
                    continue

                if line:
                    self._process_command_output(line.strip(), feedback, results)

                time.sleep(0.05)

            process_event.set()
            stdout_thread.join()
            stderr_thread.join()

            while not q.empty():
                line = q.get_nowait()
                if line:
                    self._process_command_output(line.strip(), feedback, results)

            stdout, stderr = self.process.communicate()
            if stdout:
                self._process_command_output(stdout.strip(), feedback, results)
            if stderr:
                feedback.reportError(stderr.strip())

            # Inform user whether execution was successful or not
            if self.process.returncode != 0:
                feedback.reportError(
                    f"EIS Toolkit algorithm execution failed with error: {stderr}"
                )
            else:
                feedback.pushInfo("EIS Toolkit algorithm executed successfully!")

        except TerminationException as e:
            feedback.reportError(str(e))

        # Handle potential exceptions
        except Exception as e:
            feedback.reportError(f"Run failed. Error: {str(e)}")
            try:
                self.process.terminate()
            except UnboundLocalError:
                pass
            return {}
        
        finally:
            # Ensure the subprocess is properly cleaned up in all cases
            if self.process and self.process.poll() is None:
                self.process.terminate()
                self.process.wait()  # Ensure the process is reaped

            if self.process.stdout:
                self.process.stdout.close()
            if self.process.stderr:
                self.process.stderr.close()

        return results


    def _process_command_output(self, stdout_line: str, feedback: QgsProcessingFeedback, results: Dict) -> None:
        if self.PROGRESS_PREFIX in stdout_line:
            self._update_progress(stdout_line, feedback)

        elif self.RESULTS_PREFIX in stdout_line:
            self._update_results(stdout_line, results, feedback)

        elif self.OUT_RASTERS_PREFIX in stdout_line:
            self._update_out_rasters(stdout_line)

        else:
            feedback.pushInfo(stdout_line)
