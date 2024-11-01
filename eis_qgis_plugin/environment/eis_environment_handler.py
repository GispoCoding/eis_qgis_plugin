import os
import subprocess
from typing import List, Tuple


class EnvironmentHandler:
    """Parent class for VenvEnvironmentHandler and DockerEnvironmentHandler."""

    EIS_CLI_MODULE = "eis_toolkit.cli"

    def assemble_cli_cmd() -> List[str]:
        raise NotImplementedError
    
    def get_invocation_cmd() -> List[str]:
        raise NotImplementedError

    def verify_environment() -> Tuple[bool, str]:
        raise NotImplementedError
    
    def verify_toolkit(required_version: str, env) -> Tuple[bool, str]:
        raise NotImplementedError
    
    def upgrade_toolkit(self, env) -> Tuple[bool, str]:
        raise NotImplementedError


class DockerEnvironmentHandler(EnvironmentHandler):
    """Environment handler for Docker.
    
    Makes some assumptions, for example that the image includes Poetry env with EIS Toolkit in it."""

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
        # if DEBUG:
        #     print("Mounted host folder") if mount_host_cmd is not [] else print("Did not mount host folder")
        #     print("Mounted temp folder") if mount_temp_cmd is not [] else print("Did not mount temp folder")
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
                # if DEBUG:
                #     print(f"Path: {argument} replaced with {modified_path_argument} for Docker call")

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


    def verify_toolkit(self, required_version: str, env) -> Tuple[bool, str]:
        """
        Verifies if EIS Toolkit is installed and checks if the installed version matches the required version.
        
        Args:
            required_version: The version of EIS Toolkit required by the plugin.
            env: The environment variables to pass to the subprocess (to avoid QGIS interference).

        Returns:
            A tuple where the first element is a boolean indicating success, and
            the second element is a message describing the result.
        """
        try:
            cmd = [
                self.docker_path, "run", "--rm", self.image_name, "poetry", "run", "python", "-m",
                "pip", "show", "eis_toolkit"
            ]
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )

            if result.returncode != 0:
                return False, f"EIS Toolkit is not installed in the Docker image '{self.image_name}."

            # Parse the output to extract the version of EIS Toolkit
            version = None
            for line in result.stdout.splitlines():
                if line.startswith("Version:"):
                    version = line.split("Version:")[1].strip()

            if version is None:
                return False, "EIS Toolkit version information could not be retrieved."

            if version != required_version:
                return (
                    False,
                    f"EIS Toolkit version {version} is installed, but version {required_version} is required."
                )

            return True, f"EIS Toolkit version {version} is correctly installed."

        except subprocess.CalledProcessError as e:
            return False, f"EIS Toolkit is not installed in the Docker image '{self.image_name}'. Error: {e.stderr}"


    def upgrade_toolkit(self, env) -> Tuple[bool, str]:
        """
        Upgrades EIS Toolkit to the latest version in the specified Docker image.

        Args:
            env: Environment variables to pass to the subprocess (to avoid QGIS interference).

        Returns:
            A tuple where the first element is a boolean indicating success, and
            the second element is a message describing the result.
        """
        try:
            cmd = [
                self.docker_path, "run", "--rm", self.image_name, "poetry", "run", "python", "-m",
                "pip", "install", "eis_toolkit", "--upgrade"
            ]
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                env=env
            )

            if result.returncode == 0:
                return True, "EIS Toolkit was successfully upgraded in the Docker image."
            else:
                return False, f"Failed to upgrade EIS Toolkit in the Docker image: {result.stderr}"

        except subprocess.CalledProcessError as e:
            return False, f"Failed to upgrade EIS Toolkit in the Docker image: {e.stderr}"


class VenvEnvironmentHandler(EnvironmentHandler):
    """Environment handler for Python virtual environments.
    
    Should work with venv and conda environments."""

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


    def verify_toolkit(self, required_version: str, env) -> Tuple[bool, str]:
        """
        Verifies if EIS Toolkit is installed and checks if the installed version matches the required version.
        
        Args:
            required_version: The version of EIS Toolkit required by the plugin.
            env: The environment variables to pass to the subprocess (to avoid QGIS interference).

        Returns:
            A tuple where the first element is a boolean indicating success, and
            the second element is a message describing the result.
        """
        try:
            cmd = [self.python_path, "-m", "pip", "show", "eis_toolkit"]
            creationflags = 0
            if os.name == 'nt':  # If Windows, prevent process window creation
                creationflags = subprocess.CREATE_NO_WINDOW
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                creationflags=creationflags,
                env=env
            )

            if result.returncode != 0:
                return False, "EIS Toolkit is not installed in the specified venv."

            # Parse the output to extract the version of EIS Toolkit
            version = None
            for line in result.stdout.splitlines():
                if line.startswith("Version:"):
                    version = line.split("Version:")[1].strip()

            if version is None:
                return False, "EIS Toolkit version information could not be retrieved."

            if version != required_version:
                return (
                    False,
                    f"EIS Toolkit version {version} is installed, but version {required_version} is required."
                )

            return True, f"EIS Toolkit version {version} is correctly installed."

        except subprocess.CalledProcessError as e:
            return False, f"EIS Toolkit is not installed in the specified venv. Error: {e.stderr}"


    def upgrade_toolkit(self, env) -> Tuple[bool, str]:
        """
        Upgrades EIS Toolkit to the latest version in the specified virtual environment.

        Args:
            env: Environment variables to pass to the subprocess (to avoid QGIS interference).

        Returns:
            A tuple where the first element is a boolean indicating success, and
            the second element is a message describing the result.
        """
        try:
            cmd = [self.python_path, "-m", "pip", "install", "eis_toolkit", "--upgrade"]
            creationflags = 0
            if os.name == 'nt':  # If Windows, prevent process window creation
                creationflags = subprocess.CREATE_NO_WINDOW
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                creationflags=creationflags,
                env=env
            )

            if result.returncode == 0:
                return True, "EIS Toolkit was successfully upgraded."
            else:
                return False, f"Failed to upgrade EIS Toolkit: {result.stderr}"

        except subprocess.CalledProcessError as e:
            return False, f"Failed to upgrade EIS Toolkit: {e.stderr}"
