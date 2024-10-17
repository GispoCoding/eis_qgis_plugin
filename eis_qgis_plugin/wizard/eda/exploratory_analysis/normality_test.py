from qgis.core import QgsMapLayer
from qgis.PyQt.QtWidgets import QGroupBox, QPushButton, QSpinBox, QWidget

from eis_qgis_plugin.wizard.eda.exploratory_analysis.exploratory_analysis_template import EISExploratoryAnalysis


class EISWizardNormalityTest(EISExploratoryAnalysis):
    """
    Class for normality test.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # DECLARE TYPES
        self.normality_test_page: QWidget
        self.decimals: QSpinBox
        self.compute_btn: QPushButton
        self.results_box: QGroupBox

        self.compute_btn.clicked.connect(self.perform_test)


    def _update_layer(self, layer):
        """Update (set/add items) widgets based on selected layer."""
        raise NotImplementedError("Update layer needs to be defined in child class.")
    

    def perform_test(self):
        self.clear_results_box()
        # self._check_valid_layer_type(layer)
        self.perform_normality_test()


    def perform_normality_test(self, layer: QgsMapLayer):
        raise NotImplementedError("This function needs to be defined in child class.")

    
    def clear_results_box(self):
        layout = self.results_box.layout()
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

