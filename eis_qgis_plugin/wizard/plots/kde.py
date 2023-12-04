import seaborn as sns
from qgis.core import QgsMapLayer
from qgis.gui import QgsColorButton, QgsFieldComboBox, QgsMapLayerComboBox, QgsOpacityWidget, QgsRasterBandComboBox
from qgis.PyQt.QtWidgets import QComboBox, QDoubleSpinBox, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.plots.utils import check_colors, raster_layer_to_array, str_to_bool, vector_layer_to_df

FORM_CLASS: QWidget = load_ui("wizard_plot_kde.ui")


class EISWizardKde(QWidget, FORM_CLASS):

    kde_layer: QgsMapLayerComboBox
    kde_raster_X: QgsRasterBandComboBox
    kde_vector_X: QgsFieldComboBox

    kde_color_field: QgsFieldComboBox
    kde_color: QgsColorButton
    kde_opacity: QgsOpacityWidget
    kde_log_scale: QComboBox
    kde_fill: QComboBox
    kde_multiple: QComboBox
    kde_bw_adjust: QDoubleSpinBox


    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.kde_layer.layerChanged.connect(self.update_layer)
        self.update_layer(self.kde_layer.currentLayer())


    def update_layer(self, layer):
        if layer is None:
            return

        if layer.type() == QgsMapLayer.VectorLayer:
            self.kde_raster_X.hide()

            self.kde_vector_X.setLayer(layer)
            self.kde_vector_X.show()

            self.kde_color_field.setLayer(layer)
            self.kde_color_field.setEnabled(True)

        elif layer.type() == QgsMapLayer.RasterLayer:
            self.kde_vector_X.hide()
            self.kde_color_field.setEnabled(False)

            self.kde_raster_X.setLayer(layer)
            self.kde_raster_X.show()


    def plot(self, ax):
        layer = self.kde_layer.currentLayer()

        if layer.type() == QgsMapLayer.VectorLayer:
            X_field_name = self.kde_vector_X.currentField()
            color_field_name = self.kde_color_field.currentField()
            fields = [X_field_name] + ([color_field_name] if color_field_name else [])

            df = vector_layer_to_df(layer, *fields)

            if color_field_name:
                check_colors(df[color_field_name], 10)

            layer_specific_kwargs = {
                "data": df,
                "x": X_field_name,
                "hue": color_field_name if color_field_name else None,
                "multiple": self.kde_multiple.currentText().lower(),
                "palette": "dark" if color_field_name else None
            }

        elif layer.type() == QgsMapLayer.RasterLayer:
            data = raster_layer_to_array(layer)

            layer_specific_kwargs = {
                "data": data
            }

        else:
            raise Exception(f"Unexpected layer type: {layer.type()}")

        sns.kdeplot(
            **layer_specific_kwargs,
            color=self.kde_color.color().getRgbF(),
            alpha=self.kde_opacity.opacity(),
            log_scale=str_to_bool(self.kde_log_scale.currentText()),
            fill=str_to_bool(self.kde_fill.currentText()),
            bw_adjust=self.kde_bw_adjust.value(),
            ax=ax
        )


    def plot_example(self, ax):
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
        pass
