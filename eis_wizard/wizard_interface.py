import subprocess
from typing import Tuple

from qgis.core import QgsRasterLayer, QgsProject
from PyQt5.QtCore import QFileInfo


class EISWizardInterface:

    def __init__(self, dlg, iface, plugin) -> None:
        self.dlg = dlg
        self.iface = iface
        self.plugin = plugin

    def run_toolkit_function(self, arguments):
        output, err = self.call_toolkit(
            self.plugin.python_path, self.plugin.toolkit_interface_path, arguments
        )
        self.process_output(output, err)

    def process_output(self, output: str, err: str):
        pieces = output.split(";")
        if pieces[0] == "output_path":
            path = pieces[1].strip()
            self.load_raster(path)
        
        if err != "":
            print(err)

    def load_raster(self, raster_path):
        fileInfo = QFileInfo(raster_path)
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()

        layer = QgsRasterLayer(path, baseName)
        QgsProject.instance().addMapLayer(layer)

        if layer.isValid() is True:
            self.plugin.log("Output layer was loaded successfully!")
        else:
            self.plugin.log("Unable to read basename and file path - Your string is probably invalid")

    def call_toolkit(
        self, python_path: str, toolkit_interface_path: str, arguments: list[str] = []
        ) -> Tuple[str, str]:
        """Function that handles calls to EIS Toolkit interface via subprocess module.

        Args:
            python_path (str): Path to Python (venv or other) with EIS Toolkit installed.
            function_file_path (str): Path to Python file of EIS Toolkit that receives subprocess calls.
            arguments (list[str]): List of arguments passed to the EIS Toolkit function called.

        Returns:
            output (str): Output handed by the EIS Toolkit function caller.
            error (str): Error handed by the EIS Toolkit function caller.

        Raises: To be implemented.
        """

        # NOTE: Run might be sufficient, but Popen will be more powerful if more options are needed
        # NOTE 2: Do we want return to be bytes or str? Now str

        process = subprocess.run(
            [python_path, toolkit_interface_path] + arguments,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = process.stdout
        error = process.stderr
        self.plugin.log(f"Toolkit called, response: {output}, err: {error}")
        return output, error
