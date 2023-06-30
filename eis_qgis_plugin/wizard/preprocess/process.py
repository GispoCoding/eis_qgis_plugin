from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QDialog = load_ui("preprocess/process.ui")

class EISWizardPreprocessProcess(QDialog, FORM_CLASS):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)