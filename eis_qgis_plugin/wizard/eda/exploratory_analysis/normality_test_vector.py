from qgis import processing
from qgis.core import Qgis, QgsMapLayerProxyModel
from qgis.gui import QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import QFormLayout, QLabel, QLineEdit, QListWidget, QPushButton, QWidget
from qgis.utils import iface

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.eda.exploratory_analysis.normality_test import EISWizardNormalityTest

FORM_CLASS: QWidget = load_ui("eda/wizard_normality_test_vector.ui")

class EISWizardNormalityTestVector(EISWizardNormalityTest, FORM_CLASS):
    """
    Class for normality test (vector).
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # DECLARE TYPES
        self.layer: QgsMapLayerComboBox
        self.fields: QListWidget
        self.select_all_btn: QPushButton
        self.deselect_all_btn: QPushButton

        self.select_all_btn.clicked.connect(self.fields.selectAll)
        self.deselect_all_btn.clicked.connect(self.fields.clearSelection)

        self.layer.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.layer.layerChanged.connect(self._update_layer)
        self._update_layer(self.layer.currentLayer())

        self.compute_btn.clicked.connect(self.perform_test)


    def _update_layer(self, layer):
        """Update (set/add items) widgets based on selected layer."""
        if layer is None:
            return
        self.fields.clear()
        for field in layer.fields():
            if field.isNumeric():
                self.fields.addItem(field.name())


    def perform_normality_test(self):
        normality_test_results = processing.run(
            "eis:normality_test_vector",
            {
                "input_vector": self.layer.currentLayer(),
                "columns": [item.text() for item in self.fields.selectedItems()]
            }
        )
    
        # Check if dictionary is empty = processing failed
        if not normality_test_results:
            iface.messageBar().pushMessage("Error", "Computing descriptive statistics failed.", level=Qgis.Critical)

        # Display results
        decimals = self.decimals.value()
        form_layout = QFormLayout()

        for column_name, stats in normality_test_results.items():
            column_label = QLabel(f"{column_name}:")
            form_layout.addRow(column_label)

            for stat, value in stats.items():
                stat_label = QLabel(stat)
                value_field = QLineEdit()
                if value:
                    if decimals > 0:
                        str_value = str(round(value, decimals))
                    else:
                        str_value = str(int(round(value, decimals)))
                else:
                    str_value= ""
                value_field.setText(str_value)
                form_layout.addRow(stat_label, value_field)

        # Clear any existing layout
        if self.results_box.layout() is not None:
            old_layout = self.results_box.layout()
            # Detach the old layout by assigning it to a temporary QWidget
            QWidget().setLayout(old_layout)

        self.results_box.setLayout(form_layout)


