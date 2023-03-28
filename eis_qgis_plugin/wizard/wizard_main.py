from PyQt5.QtWidgets import QDialog
from qgis.gui import QgisInterface
from qgis.PyQt import QtWidgets

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.wizard_preprocess import EISWizardPreprocess
from eis_qgis_plugin.wizard.wizard_explore import EISWizardExplore

FORM_CLASS: QDialog = load_ui("wizard_main_window.ui")


class EISWizardMain(QtWidgets.QWizard, FORM_CLASS):
    def __init__(self, iface: QgisInterface) -> None:
        super().__init__()
        self.setupUi(self)
        self.iface = iface

    #     self.preprocess_window = EISWizardPreprocess(self.iface)
    #     self.explore_window = EISWizardExplore(self.iface)
    #     self.preprocessButton.clicked.connect(self.show_preprocess)
    #     self.exploreButton.clicked.connect(self.show_explore)

    # def show_preprocess(self):
    #     self.preprocess_window.show()

    # def show_explore(self):
    #     self.explore_window.show()
