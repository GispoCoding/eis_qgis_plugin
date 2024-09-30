from qgis.PyQt.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from eis_qgis_plugin.wizard.eda.plotting import EISWizardPlotting
from eis_qgis_plugin.wizard.eda.statistics import EISWizardStatistics


class EISWizardEvaluation(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.evaluation_tabs = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.evaluation_tabs)
        self.setLayout(layout)

        # 1. Plotting / charts page
        self.plot_page = EISWizardPlotting(self)
        self.evaluation_tabs.addTab(self.plot_page, "Plots")
        
        # 2. Statistics page
        self.stats_page = EISWizardStatistics(self)
        self.evaluation_tabs.addTab(self.stats_page, "Statistics")