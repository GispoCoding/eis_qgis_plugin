import seaborn as sns
from qgis.core import QgsMapLayer
from qgis.gui import (
    QgsCollapsibleGroupBox,
    QgsColorButton,
    QgsFieldComboBox,
    QgsMapLayerComboBox,
    QgsOpacityWidget,
    QgsRasterBandComboBox,
)
from qgis.PyQt.QtWidgets import QComboBox, QDoubleSpinBox, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.plots.plot_template import EISPlot

FORM_CLASS: QWidget = load_ui("explore/wizard_plot_kde.ui")


class EISWizardKde(EISPlot, FORM_CLASS):
    """
    Class for EIS-Seaborn kdeplots.

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    layer: QgsMapLayerComboBox
    raster_X: QgsRasterBandComboBox
    vector_X: QgsFieldComboBox

    parameter_box: QgsCollapsibleGroupBox
    color_field: QgsFieldComboBox
    color: QgsColorButton
    opacity: QgsOpacityWidget
    log_scale: QComboBox
    fill: QComboBox
    multiple: QComboBox
    bw_adjust: QDoubleSpinBox


    def __init__(self, parent=None) -> None:
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
                "multiple": self.multiple.currentText().lower(),
                "palette": "dark" if color_field_name else None
            }

        elif layer.type() == QgsMapLayer.RasterLayer:
            data = self.raster_layer_to_array(layer)

            layer_specific_kwargs = {
                "data": data
            }

        else:
            raise Exception(f"Unexpected layer type: {layer.type()}")

        sns.kdeplot(
            **layer_specific_kwargs,
            color=self.color.color().getRgbF(),
            alpha=self.opacity.opacity(),
            log_scale=self.str_to_bool(self.log_scale.currentText()),
            fill=self.str_to_bool(self.fill.currentText()),
            bw_adjust=self.bw_adjust.value(),
            ax=ax
        )


    def plot_example(self, ax):
        """Produce example plot using SNS data."""
        penguins = sns.load_dataset("penguins")

        sns.kdeplot(
            data=penguins,
            x="flipper_length_mm",
            hue="species",
            multiple="stack",
            palette="dark",
            ax=ax
        )


    def reset(self):
        """Reset parameters to defaults."""
        super().reset()

        self.color_field.setField("")
        self.opacity.setOpacity(100)
        self.log_scale.setCurrentIndex(0)
        self.fill.setCurrentIndex(0)
        self.multiple.setCurrentIndex(0)
        self.bw_adjust.setValue(1.0)
