from qgis.core import QgsMapLayer
from qgis.gui import QgsColorButton, QgsFieldComboBox, QgsOpacityWidget, QgsRasterBandComboBox
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QWidget,
)

import eis_qgis_plugin.libs.seaborn as sns
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.plots.plot_template import EISPlot

FORM_CLASS: QWidget = load_ui("explore/wizard_plot_ecdf.ui")


class EISWizardEcdf(EISPlot, FORM_CLASS):
    """
    Class for EIS-Seaborn ecdfplots.

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    def __init__(self, parent=None) -> None:
        
        # DECLARE TYPES
        self.raster_X: QgsRasterBandComboBox
        self.vector_X: QgsFieldComboBox

        self.color_field: QgsFieldComboBox
        self.color: QgsColorButton
        self.opacity: QgsOpacityWidget
        self.log_scale: QComboBox
        self.stat: QComboBox

        # Initialize
        self.collapsed_height = 170
        super().__init__(parent)


    def update_layer(self, layer):
        """Update (set/show/hide) widgets based on selected layer."""
        if layer is None:
            return

        if layer.type() == QgsMapLayer.VectorLayer:
            self.raster_X.hide()

            self.vector_X.setLayer(layer)
            self.vector_X.show()

            self.color_field.setLayer(layer)
            self.color_field.setEnabled(True)

        elif layer.type() == QgsMapLayer.RasterLayer:
            self.vector_X.hide()
            self.color_field.setEnabled(False)

            self.raster_X.setLayer(layer)
            self.raster_X.show()


    def plot(self, ax):
        """Plot to given axis."""
        layer = self.layer.currentLayer()

        if layer.type() == QgsMapLayer.VectorLayer:
            X_field_name = self.vector_X.currentField()
            color_field_name = self.color_field.currentField()
            fields = [X_field_name] + ([color_field_name] if color_field_name else [])

            df = self.vector_layer_to_df(layer, *fields)

            if color_field_name:
                self.check_unique_values(df, color_field_name, 10)

            layer_specific_kwargs = {
                "data": df,
                "x": X_field_name,
                "hue": color_field_name if color_field_name else None,
                "palette": "dark" if color_field_name else None
            }

        elif layer.type() == QgsMapLayer.RasterLayer:
            data = self.raster_layer_to_array(layer)

            layer_specific_kwargs = {
                "data": data
            }

        else:
            raise Exception(f"Unexpected layer type: {layer.type()}")

        sns.ecdfplot(
            **layer_specific_kwargs,
            color=self.color.color().getRgbF(),
            alpha=self.opacity.opacity(),
            log_scale=self.str_to_bool(self.log_scale.currentText()),
            stat=self.stat.currentText().lower(),
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
        super().reset()

        self.color_field.setField("")
        self.opacity.setOpacity(100)
        self.log_scale.setCurrentIndex(0)
        self.stat.setCurrentIndex(0)
