from qgis.PyQt.QtWidgets import QDialog, QWizard

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

# from eis_qgis_plugin.wizard.explore.wizard_explore import EISWizardExplore
# from eis_qgis_plugin.wizard.preprocess.wizard_preprocess import EISWizardPreprocess

FORM_CLASS: QDialog = load_ui("model/model_dialog_wizard.ui")


class EISWizardModeling(QWizard, FORM_CLASS):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
