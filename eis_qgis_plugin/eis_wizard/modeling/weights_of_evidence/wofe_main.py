from qgis.PyQt.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from eis_qgis_plugin.eis_wizard.modeling.weights_of_evidence.calculate_responses import EISWofeCalculateResponses
from eis_qgis_plugin.eis_wizard.modeling.weights_of_evidence.calculate_weights import EISWofeCalculateWeights
from eis_qgis_plugin.eis_wizard.modeling.weights_of_evidence.conditional_independence_test import (
    EISWofeConditionalIndependence,
)


class EISWizardWeightsOfEvidence(QWidget):
    """Weights of evidence main widget."""
    
    def __init__(self, parent) -> None:
        super().__init__(parent)

        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.setLayout(layout)

        self.calculate_weights_tab = EISWofeCalculateWeights(self.tabs)
        self.tabs.addTab(self.calculate_weights_tab, "Calculate weights")

        self.calculate_responses_tab = EISWofeCalculateResponses(self.tabs)
        self.tabs.addTab(self.calculate_responses_tab, "Calculate responses")

        self.conditional_independence_test = EISWofeConditionalIndependence(self.tabs)
        self.tabs.addTab(self.conditional_independence_test, "Conditional independence test")
