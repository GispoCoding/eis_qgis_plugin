from qgis import processing
from qgis.core import NULL, QgsFieldProxyModel, QgsMapLayer
from qgis.gui import QgsFieldComboBox, QgsRasterBandComboBox, QgsSpinBox
from qgis.PyQt.QtWidgets import QLineEdit, QPushButton, QWidget

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

        # Connect layer change updates and populate initial layer
        self.layer.layerChanged.connect(self.update_layer)
        self.update_layer(self.layer.currentLayer())
        self.field.setFilters(QgsFieldProxyModel.Filter.Numeric)

        self.compute_btn.clicked.connect(self.compute_statistics)


    def update_layer(self, layer: QgsMapLayer):
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
        self.compute_general_statistics(layer)
        self.compute_descriptive_statistics_and_quantiles(layer)


    def compute_general_statistics(self, layer: QgsMapLayer):
        if layer.type() == QgsMapLayer.VectorLayer:
            field = self.field.currentField()
            all_values = [feature.attribute(field) for feature in layer.getFeatures()]
            n_total = len(all_values)
            n_null = len([value for value in all_values if value == NULL])
            # nr_of_valids = nr_of_all_values - nr_of_nulls

        elif layer.type() == QgsMapLayer.RasterLayer:
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

        else:
            raise Exception(f"Unknown layer type: {layer.type()}")  # TODO: Convert to Qgis msg

        self.n_total.setText(str(n_total))
        self.n_null.setText(str(n_null))


    def compute_descriptive_statistics_and_quantiles(self, layer: QgsMapLayer):
        # Get descriptive statistics and quantiles

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
                    "input_file": self.layer.currentLayer(),
                    #TODO band
                },
            )

        descriptive_statistics_results["variance"] = pow(descriptive_statistics_results["standard_deviation"], 2)
        decimals = self.decimals.value()
        rounded_str_dict = {
            k: str(round(v, decimals))
            if decimals > 0 else str(int(round(v, decimals)))
            for k, v in descriptive_statistics_results.items()
        }

        self.mean.setText(rounded_str_dict["mean"])
        self.standard_deviation.setText(rounded_str_dict["standard_deviation"])
        self.relative_standard_deviation.setText(rounded_str_dict["relative_standard_deviation"])
        self.variance.setText(rounded_str_dict["variance"])
        self.skewness.setText(rounded_str_dict["skew"])

        self.min.setText(rounded_str_dict["min"])
        self.quantile_25.setText(rounded_str_dict["25%"])
        self.median.setText(rounded_str_dict["50%"])
        self.quantile_75.setText(rounded_str_dict["75%"])
        self.max.setText(rounded_str_dict["max"])
