from qgis.PyQt.QtWidgets import (
    QDialog,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QDialog = load_ui("results/wizard_model_evaluation_2.ui")


class EISWizardResults(QWidget, FORM_CLASS):   

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
