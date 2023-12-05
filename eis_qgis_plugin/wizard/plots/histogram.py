import seaborn as sns
from qgis.core import QgsMapLayer
from qgis.gui import QgsColorButton, QgsFieldComboBox, QgsMapLayerComboBox, QgsOpacityWidget, QgsRasterBandComboBox
from qgis.PyQt.QtWidgets import QComboBox, QSpinBox, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.plots.utils import (
    check_colors,
    raster_layer_to_array,
    str_to_bool,
    vector_layer_to_df,
)

FORM_CLASS: QWidget = load_ui("wizard_plot_histogram.ui")



class EISWizardHistogram(QWidget, FORM_CLASS):
    """
    Class for EIS-Seaborn histograms (histplots).

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    histogram_layer: QgsMapLayerComboBox
    histogram_raster_X: QgsRasterBandComboBox
    histogram_vector_X: QgsFieldComboBox

    histogram_color_field: QgsFieldComboBox
    histogram_color: QgsColorButton
    histogram_opacity: QgsOpacityWidget
    histogram_log_scale: QComboBox
    histogram_fill: QComboBox
    histogram_multiple: QComboBox
    histogram_stat: QComboBox
    histogram_element: QComboBox
    histogram_nr_of_bins: QSpinBox


    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.histogram_layer.layerChanged.connect(self.update_layer)
        self.update_layer(self.histogram_layer.currentLayer())

        self.settings_page = self.parent().parent().settings_page
        self.reset()

    def _set_deafult_color(self):
        """Fetch default color from settings and set color widget selection."""
        self.histogram_color.setColor(self.settings_page.get_default_color())

    def update_layer(self, layer: QgsMapLayer):
        """Update (set/show/hide) widgets based on selected layer."""
        if layer is None:
            return

        if layer.type() == QgsMapLayer.VectorLayer:
            self.histogram_raster_X.hide()

            self.histogram_vector_X.setLayer(layer)
            self.histogram_vector_X.show()

            self.histogram_color_field.setLayer(layer)
            self.histogram_color_field.setEnabled(True)

        elif layer.type() == QgsMapLayer.RasterLayer:
            self.histogram_vector_X.hide()
            self.histogram_color_field.setEnabled(False)

            self.histogram_raster_X.setLayer(layer)
            self.histogram_raster_X.show()

    def plot(self, ax):
        """Plot to given axis."""
        layer = self.histogram_layer.currentLayer()

        if layer.type() == QgsMapLayer.VectorLayer:
            X_field_name = self.histogram_vector_X.currentField()
            color_field_name = self.histogram_color_field.currentField()
            fields = [X_field_name] + ([color_field_name] if color_field_name else [])

            df = vector_layer_to_df(layer, *fields)

            if color_field_name:
                check_colors(df[color_field_name], 10)

            layer_specific_kwargs = {
                "data": df,
                "x": X_field_name,
                "hue": color_field_name if color_field_name else None,
                "multiple": self.histogram_multiple.currentText().lower(),
                "palette": "dark" if color_field_name else None
            }

        elif layer.type() == QgsMapLayer.RasterLayer:
            data = raster_layer_to_array(layer)

            layer_specific_kwargs = {
                "data": data
            }

        else:
            raise Exception(f"Unexpected layer type: {layer.type()}")

        sns.histplot(
            **layer_specific_kwargs,
            color=self.histogram_color.color().getRgbF(),
            alpha=self.histogram_opacity.opacity(),
            log_scale=str_to_bool(self.histogram_log_scale.currentText()),
            fill=str_to_bool(self.histogram_fill.currentText()),
            stat=self.histogram_stat.currentText().lower(),
            element=self.histogram_element.currentText().lower(),
            bins=self.histogram_nr_of_bins.value() if self.histogram_nr_of_bins.value() > 0 else "auto",
            ax=ax
        )


    def plot_example(self, ax):
        """Produce example plot using SNS data."""
        penguins = sns.load_dataset("penguins")

        sns.histplot(
            data=penguins,
            x="flipper_length_mm",
            hue="species",
            multiple="stack",
            palette="dark",
            ax=ax
        )


    def reset(self):
        """Reset parameters to defaults."""
        self.histogram_color_field.setField("")
        self._set_deafult_color()
        self.histogram_opacity.setOpacity(100)
        self.histogram_log_scale.setCurrentIndex(0)

        self.histogram_fill.setCurrentIndex(0)
        self.histogram_multiple.setCurrentIndex(0)
        self.histogram_stat.setCurrentIndex(0)
        self.histogram_element.setCurrentIndex(0)
        self.histogram_nr_of_bins.setValue(0)
