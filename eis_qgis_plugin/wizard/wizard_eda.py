from qgis.PyQt.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from eis_qgis_plugin.wizard.eda.exploratory_analysing import EISWizardExploratoryAnalysis
from eis_qgis_plugin.wizard.eda.plotting import EISWizardPlotting


class EISWizardEDA(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.eda_tabs = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.eda_tabs)
        self.setLayout(layout)

        # 1. Plotting / charts page
        self.plot_page = EISWizardPlotting(self)
        self.eda_tabs.addTab(self.plot_page, "Plots")
        
        # 2. Statistics page
        self.stats_page = EISWizardExploratoryAnalysis(self)
        self.eda_tabs.addTab(self.stats_page, "Exploratory analysis")
