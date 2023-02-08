from PyQt5.QtWidgets import QDialog
from qgis.gui import QgisInterface, QgsFileWidget
from qgis.PyQt import QtWidgets

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QDialog = load_ui("eis_wizard_dialog_resample.ui")


class ResampleRasterDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, iface: QgisInterface) -> None:
        super().__init__()
        self.setupUi(self)
        self.iface = iface

    def get_input_file_path(self):
        pass

    def get_output_file_path(self) -> str:
        self.mQgsFileWidget: QgsFileWidget
        return self.mQgsFileWidget.filePath()

    def get_resampling_method(self):
        pass

    def get_upscale_factor(self):
        pass
