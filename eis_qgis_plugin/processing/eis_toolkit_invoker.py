import json
import os
import subprocess
import time
from typing import List, Tuple

from qgis.core import (
    QgsProcessingFeedback,
    QgsProject,
    QgsRasterLayer,
)

PROGRESS_PREFIX = "Progress:"
OUT_RASTERS_PREFIX = "Output rasters:"
RESULTS_PREFIX = "Results:"

DEBUG = True


class EISToolkitInvoker:
    """Class that handles communication between EIS QGIS plugin and EIS Toolkit."""

    def __init__(self, python_env_path, env_type = "venv"):
        """
        Initializes the EISToolkitInvoker with the path to the Python environment and its type.

        Args:
            python_env_path: Path to the Python executable or environment.
            env_type: Type of the Python environment. This determines how the CLI call is assembled.
        """
        self.python_env_path = python_env_path
        self.bin_directory = self.get_bin_directory()
        self.env_type = env_type  # Main, venv, poetry, conda, docker. Will be linked to EISSettings or elsewhere

        self.module_flag = "-m"
        self.eis_cli_module = "eis_toolkit.cli"
        self.cmd = None


    @staticmethod
    def get_bin_directory():
        """Get directory name based on OS."""
        if os.name == "nt":  # Windows
            return "Scripts"
        else:
            return "bin"


    @staticmethod
    def format_algorithm_name(alg_name: str) -> str:
        """
        Formats the algorithm name for CLI use.

        Args:
            The algorithm name to format.

        Returns:
            A formatted algorithm name suitable for CLI invocation.
        """
        return (alg_name + "_cli").replace("_", "-")


    @staticmethod
    def update_progress(stdout: str, feedback: QgsProcessingFeedback):
        """
        Updates the QGIS processing algorithm's progress based on the stdout message.

        Args:
            stdout: Standard output message from the subprocess.
            feedback: Instance of QgsProcessingFeedback to report progress to QGIS.
        """
        progress = int(stdout.split(":")[1].strip()[:-1])
        feedback.setProgress(progress)
        feedback.pushInfo(f"Progress: {progress}%")


    @staticmethod
    def update_results(stdout: str, results: dict):
        """
        Updates the results dictionary with information parsed from the stdout message.

        Args:
            stdout: Standard output message containing results in JSON format.
            results: Dictionary to store the parsed results.
        """
        # Extract the JSON part
        json_str = stdout.split(RESULTS_PREFIX)[-1].strip()

        # Deserialize the JSON-formatted string to a Python dict
        output_dict = json.loads(json_str)

        for key, value in output_dict.items():
            results[key] = value


    @staticmethod
    def update_out_rasters(stdout: str):
        """
        Updates the QGIS project with output rasters parsed from the stdout message.

        Called *only* when processing algorithm has multiple rasters outputs. Single outputs
        are handled automatically.

        Args:
            stdout: Standard output message containing paths to output rasters in JSON format.
        """
        # Extract the JSON part
        json_str = stdout.split(OUT_RASTERS_PREFIX)[-1].strip()

        # Deserialize the JSON-formatted string to a Python dict
        output_dict = json.loads(json_str)

        for name, path in output_dict.items():
            # TODO: Handle potential errors
            output_raster_layer = QgsRasterLayer(path, name)
            QgsProject.instance().addMapLayer(output_raster_layer)


    def get_python_executable_path(self):
        """
        Determines the path to the Python executable based on the environment type.

        Returns:
            The full path to the Python executable.
        """
        if self.env_type in ["venv", "conda", "poetry"]:
            return os.path.join(self.python_env_path, self.bin_directory, "python")
        
        elif self.env_type == "docker":

            # DRAFT, TODO
            # docker_command = [
            #     "docker", "run", "--rm", "--name", container_name,
            #     docker_image_name, command_to_run
            # ]

            # Placeholder for Docker support

            raise NotImplementedError("Docker environment support is not implemented yet.")
        
        else:
            raise ValueError(f"Unrecognized environment type: {self.env_type}")


    def assemble_cli_call(self, alg_name: str, typer_args: List[str], typer_options: List[str]):
        """
        Assembles command-line interface call for a specific algorithm of EIS toolkit.

        Args:
            alg_name: Name of the algorithm (in QGIS) to be invoked.
            typer_args: List of arguments for the Typer CLI.
            typer_options: List of options for the Typer CLI.
        """
        python_path = self.get_python_executable_path()
        cli_function_name = self.format_algorithm_name(alg_name)

        self.cmd = [python_path, self.module_flag, self.eis_cli_module, cli_function_name, *typer_args, *typer_options]

        if DEBUG:
            print("Assembled CLI command:", self.cmd)


    def run(self, feedback: QgsProcessingFeedback) -> dict:
        """
        Executes the assembled CLI call of the EIS toolkit using subprocess.

        Args:
            feedback: Instance of QgsProcessingFeedback to report progress and messages to QGIS.

        Returns:
            A dictionary of results parsed from the CLI output.
        """
        if self.cmd is None:
            raise Exception("Assemble a CLI call before trying to run EIS Toolkit.")

        results = {}

        # Execute EIS Toolkit through subprocess
        try:
            # Open the process
            process = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )

            # Poll the subprocess to get messages and termination signal
            while process.poll() is None:
                stdout = process.stdout.readline().strip()

                if PROGRESS_PREFIX in stdout:
                    self.update_progress(stdout, feedback)
    
                elif RESULTS_PREFIX in stdout:
                    self.update_results(stdout, results)

                elif OUT_RASTERS_PREFIX in stdout:
                    self.update_out_rasters(stdout)
            
                else:
                    feedback.pushInfo(stdout)

                time.sleep(0.01)

            stdout, stderr = process.communicate()

            # Inform user whether execution was succesfull or not
            if process.returncode != 0:
                feedback.reportError(
                    f"EIS Toolkit algorithm execution failed with error: {stderr}"
                )
            else:
                feedback.pushInfo("EIS Toolkit algorithm executed successfully!")

        # Handle potential exceptions
        except Exception as e:
            feedback.reportError(f"Failed to run the command. Error: {str(e)}")
            try:
                process.terminate()
            except UnboundLocalError:
                pass
            return {}
        
        return results


    def check_environment_validity(self) -> Tuple[bool, str]:
        """
        Checks if EIS Toolkit can be found in the specified Python environment.

        Probes the environment by opening Python using subprocess and trying to import EIS Toolkit.
        
        Returns:
            True or false indicating whether EIS Toolkit was found.
            Message describing verification results.
        """
        python_executable = "python.exe" if os.name == "nt" else "python"
        python_path = os.path.join(self.python_env_path, self.get_bin_directory(), python_executable)

        # Attempt to import the toolkit using the specified Python executable
        try:
            # Construct the command to check for toolkit installation
            cmd = [python_path, "-c", "import eis_toolkit; print('Toolkit found')"]

            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            if 'Toolkit found' in result.stdout:
                return True, "Valid: EIS Toolkit found in the env."
            else:
                return False, "Invalid: Toolkit not found in the env."
        except subprocess.CalledProcessError as e:
            # Python command failed, likely because the toolkit is not installed
            return False, f"Failed to import the toolkit. Error: {e.stderr}"
