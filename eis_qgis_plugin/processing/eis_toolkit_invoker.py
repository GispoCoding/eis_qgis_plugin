import json
import logging
import os
import queue
import subprocess
import threading
import time
from typing import Dict, List, TextIO, Tuple

from qgis.core import QgsProcessingFeedback, QgsProject, QgsRasterLayer

from eis_qgis_plugin.wizard.utils.settings_manager import EISSettingsManager

DEBUG = True

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
        venv_directory = EISSettingsManager.get_venv_directory() if venv_directory is None else venv_directory
        docker_path = EISSettingsManager.get_docker_path() if docker_path is None else docker_path
        docker_image_name = (
            EISSettingsManager.get_docker_image_name() if docker_image_name is None else docker_image_name
        )
        host_folder = EISSettingsManager.get_docker_host_folder()
        temp_folder = EISSettingsManager.get_docker_temp_folder()

        if env_type == "venv":
            self.environment_handler = VenvEnvironmentHandler(venv_directory)
        elif env_type == "docker":
            self.environment_handler = DockerEnvironmentHandler(
                docker_path,
                docker_image_name,
                host_folder,
                temp_folder
            )
        else:
            raise ValueError(f"Unsupported environment type: {env_type}")

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
        feedback.setProgress(int(progress))
        feedback.pushInfo(f"Progress: {progress}%")


    def _update_results(self, stdout: str, results: dict):
        """Updates the results dictionary with information parsed from the stdout message."""
        # Extract the JSON part
        json_str = stdout.split(self.RESULTS_PREFIX)[-1].strip()

        # Deserialize the JSON-formatted string to a Python dict
        output_dict = json.loads(json_str)

        for key, value in output_dict.items():
            results[key] = value


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
        return self.environment_handler.verify_toolkit()


    
    def run_toolkit_command(self, feedback: QgsProcessingFeedback) -> Dict:
        """Runs the toolkit command and captures the output."""
        if not self.cmd:
            raise Exception("Assemble a CLI call before trying to run EIS Toolkit.")

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
            python_free_environment = {key: value for key, value in os.environ.items() if not key.startswith("PYTHON")}
            logger.debug(f'Running command "{" ".join(self.cmd)}" with environment: {python_free_environment=}')

            creationflags = 0
            if os.name == 'nt':  # If Windows, prevent process window creation
                creationflags = subprocess.CREATE_NO_WINDOW

            self.process = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                env=python_free_environment,
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
            self._update_results(stdout_line, results)

        elif self.OUT_RASTERS_PREFIX in stdout_line:
            self._update_out_rasters(stdout_line)

        else:
            feedback.pushInfo(stdout_line)


class EnvironmentHandler:

    EIS_CLI_MODULE = "eis_toolkit.cli"

    def assemble_cli_cmd() -> List[str]:
        raise NotImplementedError
    
    def get_invocation_cmd() -> List[str]:
        raise NotImplementedError

    def verify_environment() -> Tuple[bool, str]:
        raise NotImplementedError
    
    def verify_toolkit() -> Tuple[bool, str]:
        raise NotImplementedError


class DockerEnvironmentHandler(EnvironmentHandler):

    DOCKER_DATA_FOLDER = "/data_folder"
    DOCKER_TEMP_FOLDER = "/temp"

    def __init__(self, docker_path: str, image_name: str, host_folder: str, temp_folder: str) -> None:
        self.docker_path = docker_path
        self.image_name = image_name
        self.host_folder = host_folder
        self.temp_folder = temp_folder

        self.mount_host = False
        self.mount_temp = False


    def assemble_cli_cmd(self, alg_name: str, typer_args: List[str], typer_options: List[str]):
        typer_args = self.modify_paths(typer_args)
        typer_options = self.modify_paths(typer_options)

        return [
            *self.get_invocation_cmd(),
            self.EIS_CLI_MODULE,
            alg_name,
            *typer_args,
            *typer_options
        ]


    def get_invocation_cmd(self) -> List[str]:
        mount_host_cmd = ["-v", f"{self.host_folder}:{self.DOCKER_DATA_FOLDER}"] if self.mount_host else []
        mount_temp_cmd = ["-v", f"{self.temp_folder}:{self.DOCKER_TEMP_FOLDER}"] if self.mount_temp else []
        if DEBUG:
            print("Mounted host folder") if mount_host_cmd is not [] else print("Did not mount host folder")
            print("Mounted temp folder") if mount_temp_cmd is not [] else print("Did not mount temp folder")
        cmd = [
            self.docker_path,
            "run",
            "--rm",
            *mount_host_cmd,
            *mount_temp_cmd,
            self.image_name,
            "poetry",
            "run",
            "python",
            "-m"
        ]
        return cmd


    def modify_paths(self, arguments: List[str]) -> List[str]:
        """Modify path arguments to match container directory and convert path Windows -> Unix."""
        for i, argument in enumerate(arguments):
            if "/" in argument or "\\" in argument:
                if self.host_folder in argument:
                    modified_path_argument = argument.replace(self.host_folder, self.DOCKER_DATA_FOLDER)
                    self.mount_host = True
                elif self.temp_folder in argument:
                    modified_path_argument = argument.replace(self.temp_folder, self.DOCKER_TEMP_FOLDER)
                    self.mount_temp = True
                else:
                    raise ValueError(f"Parameter path points to a folder not specified for Docker: {argument}")
                modified_path_argument = modified_path_argument.replace("\\", "/")
                arguments[i] = modified_path_argument
                if DEBUG:
                    print(f"Path: {argument} replaced with {modified_path_argument} for Docker call")

        return arguments


    def verify_environment(self) -> Tuple[bool, str]:
        if self.image_name == "":
            return False, "Docker image not specified."

        # 1. Check if Docker is available
        try:
            cmd = [self.docker_path, "--version"]
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except FileNotFoundError:
            return False, f"Docker not found at '{self.docker_path}'"
        except subprocess.CalledProcessError as e:
            return False, f"Docker is installed but cannot be executed. Error: {e.stderr}"

        # 2. Check if the Docker image exists
        try:
            cmd = [self.docker_path, "image", "inspect", self.image_name]
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return True, "Docker installation OK and image found."
        except subprocess.CalledProcessError:
            return False, f"Docker image '{self.image_name}' not found."


    def verify_toolkit(self) -> Tuple[bool, str]:
        try:
            cmd = [
                self.docker_path, "run", "--rm", self.image_name, "poetry", "run", "python", "-c", "import eis_toolkit"
            ]
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return True, f"EIS Toolkit is installed in the Docker image '{self.image_name}'."
        except subprocess.CalledProcessError as e:
            return False, f"EIS Toolkit is not installed in the Docker image '{self.image_name}'. Error: {e.stderr}"


class VenvEnvironmentHandler(EnvironmentHandler):

    def __init__(self, venv_directory: os.PathLike) -> None:
        self.venv_directory = venv_directory
        self.python_path = self.get_python_path(venv_directory)


    def assemble_cli_cmd(self, alg_name: str, typer_args: List[str], typer_options: List[str]):
        return [
            *self.get_invocation_cmd(),
            self.EIS_CLI_MODULE,
            alg_name,
            *typer_args,
            *typer_options
        ]

    @staticmethod
    def get_python_path(venv_directory: os.PathLike) -> str:
        # os_name = platform.system().lower()
        is_windows = os.name == "nt"
        exe_directory = "Scripts" if is_windows else "bin"
        python_executable = "python.exe" if is_windows else "python"

        # Heuristic to check if Conda env
        if os.path.exists(os.path.join(venv_directory, 'conda-meta')) and is_windows:
            return os.path.join(venv_directory, python_executable)
        else:
            return os.path.join(venv_directory, exe_directory, python_executable)
            

    def get_invocation_cmd(self) -> List[str]:
        return [self.python_path, "-m"]


    def verify_environment(self) -> Tuple[bool, str]:
        if self.venv_directory == "":
            return False, "Venv directory not specified."
        if os.path.exists(self.python_path):
            return True, "Venv directory is OK."
        else:
            return False, "Venv directory is invalid."


    def verify_toolkit(self) -> Tuple[bool, str]:
        try:
            cmd = [self.python_path, "-c", "import eis_toolkit"]
            creationflags = 0
            if os.name == 'nt':  # If Windows, prevent process window creation
                creationflags = subprocess.CREATE_NO_WINDOW
            subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                creationflags=creationflags
            )
            return True, "EIS Toolkit is installed in the specified venv."
        except subprocess.CalledProcessError as e:
            return False, f"EIS Toolkit is not installed in the specified venv. Error: {e.stderr}"
