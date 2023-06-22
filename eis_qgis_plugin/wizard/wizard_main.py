from qgis.PyQt.QtWidgets import QDialog, QWizard

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
# from eis_qgis_plugin.wizard.explore.wizard_explore import EISWizardExplore
# from eis_qgis_plugin.wizard.preprocess.wizard_preprocess import EISWizardPreprocess

FORM_CLASS: QDialog = load_ui("old_designs_and_tests/wizard_main_window.ui")


class EISWizardMain(QWizard, FORM_CLASS):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

    #     self.preprocess_window = EISWizardPreprocess(self.iface)
    #     self.explore_window = EISWizardExplore(self.iface)
    #     self.preprocessButton.clicked.connect(self.show_preprocess)
    #     self.exploreButton.clicked.connect(self.show_explore)

    # def show_preprocess(self):
    #     self.preprocess_window.show()

    # def show_explore(self):
    #     self.explore_window.show()
