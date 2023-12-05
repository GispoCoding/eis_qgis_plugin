import seaborn as sns
from qgis.core import QgsMapLayer
from qgis.gui import QgsColorButton, QgsFieldComboBox, QgsMapLayerComboBox, QgsOpacityWidget, QgsRasterBandComboBox
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.plots.utils import check_colors, raster_layer_to_array, str_to_bool, vector_layer_to_df

FORM_CLASS: QWidget = load_ui("wizard_plot_ecdf.ui")


class EISWizardEcdf(QWidget, FORM_CLASS):
    """
    Class for EIS-Seaborn ecdfplots.

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    ecdf_layer: QgsMapLayerComboBox
    ecdf_raster_X: QgsRasterBandComboBox
    ecdf_vector_X: QgsFieldComboBox

    ecdf_color_field: QgsFieldComboBox
    ecdf_color: QgsColorButton
    ecdf_opacity: QgsOpacityWidget
    ecdf_log_scale: QComboBox
    ecdf_stat: QComboBox


    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.ecdf_layer.layerChanged.connect(self.update_layer)
        self.update_layer(self.ecdf_layer.currentLayer())

        self.settings_page = self.parent().parent().settings_page
        self.reset()

    def _set_deafult_color(self):
        """Fetch default color from settings and set color widget selection."""
        self.ecdf_color.setColor(self.settings_page.get_default_color())

    def update_layer(self, layer):
        """Update (set/show/hide) widgets based on selected layer."""
        if layer is None:
            return

        if layer.type() == QgsMapLayer.VectorLayer:
            self.ecdf_raster_X.hide()

            self.ecdf_vector_X.setLayer(layer)
            self.ecdf_vector_X.show()

            self.ecdf_color_field.setLayer(layer)
            self.ecdf_color_field.setEnabled(True)

        elif layer.type() == QgsMapLayer.RasterLayer:
            self.ecdf_vector_X.hide()
            self.ecdf_color_field.setEnabled(False)

            self.ecdf_raster_X.setLayer(layer)
            self.ecdf_raster_X.show()


    def plot(self, ax):
        """Plot to given axis."""
        layer = self.ecdf_layer.currentLayer()

        if layer.type() == QgsMapLayer.VectorLayer:
            X_field_name = self.ecdf_vector_X.currentField()
            color_field_name = self.ecdf_color_field.currentField()
            fields = [X_field_name] + ([color_field_name] if color_field_name else [])

            df = vector_layer_to_df(layer, *fields)

            if color_field_name:
                check_colors(df[color_field_name], 10)

            layer_specific_kwargs = {
                "data": df,
                "x": X_field_name,
                "hue": color_field_name if color_field_name else None,
                "palette": "dark" if color_field_name else None
            }

        elif layer.type() == QgsMapLayer.RasterLayer:
            data = raster_layer_to_array(layer)

            layer_specific_kwargs = {
                "data": data
            }

        else:
            raise Exception(f"Unexpected layer type: {layer.type()}")

        sns.ecdfplot(
            **layer_specific_kwargs,
            color=self.ecdf_color.color().getRgbF(),
            alpha=self.ecdf_opacity.opacity(),
            log_scale=str_to_bool(self.ecdf_log_scale.currentText()),
            stat=self.ecdf_stat.currentText().lower(),
            ax=ax
        )


    def plot_example(self, ax):
        """Produce example plot using SNS data."""
        penguins = sns.load_dataset("penguins")

        sns.ecdfplot(
            data=penguins,
            x="flipper_length_mm",
            hue="species",
            palette="dark",
            ax=ax
        )


    def reset(self):
        """Reset parameters to defaults."""
        self.ecdf_color_field.setField("")
        self._set_deafult_color()
        self.ecdf_opacity.setOpacity(100)
        self.ecdf_log_scale.setCurrentIndex(0)
        self.ecdf_stat.setCurrentIndex(0)
