from qgis.PyQt.QtWidgets import QDialog, QTabWidget, QWidget

from eis_qgis_plugin.eis_wizard.evaluation.plotting import EISWizardEvaluationPlotting
from eis_qgis_plugin.eis_wizard.evaluation.statistics import EISWizardEvaluationStatistics
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QDialog = load_ui("wizard_evaluation.ui")


class EISWizardEvaluation(QWidget, FORM_CLASS): 

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.evaluation_tabs: QTabWidget

        self.statistics_page = EISWizardEvaluationStatistics()
        self.plotting_page = EISWizardEvaluationPlotting()
        self.evaluation_tabs.addTab(self.statistics_page, "Statistics")
        self.evaluation_tabs.addTab(self.plotting_page, "Plotting")


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.plotting_page.update_plot_pixmap(self.evaluation_tabs.width() - 75)
