from typing import Tuple

from qgis import processing
from qgis.core import NULL, Qgis, QgsApplication, QgsFieldProxyModel, QgsMapLayer
from qgis.gui import QgsFieldComboBox, QgsRasterBandComboBox, QgsSpinBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QLineEdit, QPushButton, QWidget
from qgis.utils import iface

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QWidget = load_ui("eda/wizard_statistics.ui")


class EISWizardStatistics(QWidget, FORM_CLASS):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # DECLARE TYPES
        self.layer: QgsMapLayer
        self.band: QgsRasterBandComboBox
        self.field: QgsFieldComboBox
        self.decimals: QgsSpinBox
        self.compute_btn: QPushButton

        self.n_total: QLineEdit
        self.n_null: QLineEdit

        self.mean: QLineEdit
        self.standard_deviation: QLineEdit
        self.relative_standard_deviation: QLineEdit
        self.variance: QLineEdit
        self.skewness: QLineEdit

        self.min: QLineEdit
        self.quantile_25: QLineEdit
        self.median: QLineEdit
        self.quantile_75: QLineEdit
        self.max: QLineEdit

        # Map widgets to the processing algorithm return dictionary keys
        self.descriptive_stats_widgets = {
            "mean": self.mean,
            "standard_deviation": self.standard_deviation,
            "relative_standard_deviation": self.relative_standard_deviation,
            "variance": self.variance,
            "skew": self.skewness,
            "min": self.min,
            "25%": self.quantile_25,
            "50%": self.median,
            "75%": self.quantile_75,
            "max": self.max
        }

        # Connect layer change updates and populate initial layer
        self.layer.layerChanged.connect(self._update_layer)
        self._update_layer(self.layer.currentLayer())
        self.field.setFilters(QgsFieldProxyModel.Filter.Numeric)

        self.compute_btn.setIcon(QIcon(QgsApplication.getThemeIcon("mActionStart.svg")))
        self.compute_btn.setDefault(True)
        self.compute_btn.clicked.connect(self.compute_statistics)


    def _update_layer(self, layer: QgsMapLayer):
        """Update (set/show/hide) widgets based on selected layer."""
        if layer is None:
            return

        if layer.type() == QgsMapLayer.VectorLayer:
            self.band.hide()

            self.field.setLayer(layer)
            self.field.show()

        elif layer.type() == QgsMapLayer.RasterLayer:
            self.field.hide()

            self.band.setLayer(layer)
            self.band.show()


    def compute_statistics(self):
        layer = self.layer.currentLayer()
        self._check_valid_layer_type(layer)
        self.compute_general_statistics(layer)
        self.compute_descriptive_statistics_and_quantiles(layer)


    def _check_valid_layer_type(self, layer: QgsMapLayer) -> bool:
        if layer.type() not in [QgsMapLayer.VectorLayer, QgsMapLayer.RasterLayer]:
            iface.messageBar().pushMessage("Error", f"Unsupported layer type: {layer.type()}", level=Qgis.Critical)
            return False
        return True


    def compute_general_statistics(self, layer: QgsMapLayer):
        if layer.type() == QgsMapLayer.VectorLayer:
            n_total, n_null = self._compute_general_statistics_vector(layer)
        else:
            n_total, n_null = self._compute_general_statistics_raster(layer)
        self.n_total.setText(str(n_total))
        self.n_null.setText(str(n_null))


    def _compute_general_statistics_vector(self, layer: QgsMapLayer) -> Tuple[int, int]:
        field = self.field.currentField()
        all_values = [feature.attribute(field) for feature in layer.getFeatures()]
        n_total = len(all_values)
        n_null = len([value for value in all_values if value == NULL]) 
        # nr_of_valids = nr_of_all_values - nr_of_nulls
        return n_total, n_null  


    def _compute_general_statistics_raster(self, layer: QgsMapLayer) -> Tuple[int, int]:
        data_provider = layer.dataProvider()
        width = layer.width()
        height = layer.height()
        band = int(self.band.currentIndex())

        data_block = data_provider.block(band, layer.extent(), width, height)
        n_null = 0
        # nr_of_valids = 0
        n_total = width * height

        # Loop over all pixels
        for row in range(height):
            for col in range(width):
                pixel_value = data_block.value(row, col)
                if pixel_value == NULL:
                    n_null += 1
                else:
                    # nr_of_valids += 1
                    pass
        return n_total, n_null


    def compute_descriptive_statistics_and_quantiles(self, layer: QgsMapLayer):
        # Compute descriptive statistics (including quantiles)
        if layer.type() == QgsMapLayer.VectorLayer:
            descriptive_statistics_results = processing.run(
                "eis:descriptive_statistics_vector",
                {
                    "input_file": self.layer.currentLayer(),
                    "column": self.field.currentField(),
                },
            )
        else:
            descriptive_statistics_results = processing.run(
                "eis:descriptive_statistics_raster",
                {
                    "input_raster": self.layer.currentLayer(),
                    "band": self.band.currentBand()
                },
            )

        # Check if dictionary is empty = processing failed
        if not descriptive_statistics_results:
            iface.messageBar().pushMessage("Error", "Computing descriptive statistics failed.", level=Qgis.Critical)
        else:
            # Calculate variance 
            descriptive_statistics_results["variance"] = pow(descriptive_statistics_results["standard_deviation"], 2)

        # Update widgets
        decimals = self.decimals.value()
        for dict_key, widget in self.descriptive_stats_widgets.items():
            value = descriptive_statistics_results.get(dict_key)
            if value:
                if decimals > 0:
                    str_value = str(round(value, decimals))
                else:
                    str_value = str(int(round(value, decimals)))
            else:
                str_value = ""
            widget.setText(str_value)
