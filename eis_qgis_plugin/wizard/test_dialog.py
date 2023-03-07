from PyQt5.QtWidgets import QDialog, QWizard
from qgis.gui import QgisInterface, QgsFileWidget
from qgis.PyQt import QtWidgets

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QDialog = load_ui("wizard.ui")


class NewWizardDialog(QtWidgets.QWizard, FORM_CLASS):
    def __init__(self, iface: QgisInterface) -> None:
        super().__init__()
        self.setupUi(self)
        self.iface = iface



class PreprocessDialog(QtWidgets.QWizardPage, load_ui("preprocess_window_3.ui")):
    def __init__(self, iface: QgisInterface) -> None:
        super().__init__()
        self.setupUi(self)
        self.iface = iface
