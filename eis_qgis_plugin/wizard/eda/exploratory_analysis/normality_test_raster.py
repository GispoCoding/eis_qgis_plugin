from typing import List

from qgis import processing
from qgis.core import Qgis, QgsRasterLayer
from qgis.PyQt.QtWidgets import QFormLayout, QGroupBox, QLabel, QLineEdit, QSizePolicy, QVBoxLayout, QWidget
from qgis.utils import iface

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.layer_data_table import LayerDataTable
from eis_qgis_plugin.wizard.eda.exploratory_analysis.normality_test import EISWizardNormalityTest

FORM_CLASS: QWidget = load_ui("eda/wizard_normality_test_raster.ui")

class EISWizardNormalityTestRaster(EISWizardNormalityTest, FORM_CLASS):
    """
    Class for normality test (raster).
    """

    def __init__(self, parent=None) -> None:
        
        # DECLARE TYPES
        self.data_box: QGroupBox

        # Initialize
        super().__init__(parent)

        self.data_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.data_layer_table = LayerDataTable(self, dtype=QgsRasterLayer, field_selection=True)
        self.data_box.setLayout(QVBoxLayout())
        self.data_box.layout().addWidget(self.data_layer_table)

        self.data_layer_table.size_changed.connect(self._update_size)

        self.data_layer_table.add_row()

        self.compute_btn.clicked.connect(self.perform_test)


    def _update_size(self, size_change: int):
        self.setMinimumHeight(self.minimumHeight() + size_change)
        self.setMaximumHeight(self.maximumHeight() + size_change)


    def get_layers(self) -> List[QgsRasterLayer]:
        return [
            self.data_layer_table.cellWidget(row, 0).currentLayer() for row in range(self.data_layer_table.rowCount())
        ]
    
    def get_bands(self) -> List[int]:
        return [
            self.data_layer_table.cellWidget(row, 1).currentBand() for row in range(self.data_layer_table.rowCount())
        ]
        
    
    def perform_normality_test(self):
        input_rasters = self.get_layers()
        if len(set(input_rasters)) > 1:
            iface.messageBar().pushMessage("Use bands from one raster only!", level=Qgis.Critical)
            return
        input_raster = input_rasters[0]
        bands = self.get_bands()
        # if not bands:
        #     bands = [band for band in range(1, input_raster.bandCount() + 1)]
        
        normality_test_results = processing.run(
            "eis:normality_test_raster",
            {
                "input_raster": input_raster,
                "bands": bands
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