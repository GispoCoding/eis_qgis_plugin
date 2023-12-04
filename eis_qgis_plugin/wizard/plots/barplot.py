import seaborn as sns
from qgis.core import QgsMapLayerProxyModel
from qgis.gui import (
    QgsColorButton,
    QgsFieldComboBox,
    QgsMapLayerComboBox,
    QgsOpacityWidget,
)
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.plots.utils import check_colors, str_to_bool, vector_layer_to_df

FORM_CLASS: QWidget = load_ui("wizard_plot_barplot.ui")


class EISWizardBarplot(QWidget, FORM_CLASS):

    barplot_layer: QgsMapLayerComboBox
    barplot_X: QgsFieldComboBox
    barplot_Y: QgsFieldComboBox

    barplot_color_field: QgsFieldComboBox
    barplot_color: QgsColorButton
    barplot_opacity: QgsOpacityWidget
    barplot_log_scale: QComboBox
    barplot_estimator: QComboBox
    barplot_errorbars: QComboBox


    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.barplot_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)

        self.barplot_layer.layerChanged.connect(self.update_layer)
        self.update_layer(self.barplot_layer.currentLayer())

        # Defaults from settings
        settings = self.parent().parent().settings_page
        self.barplot_color.setColor(settings.get_default_color())


    def update_layer(self, layer):
        if layer is None:
            return

        self.barplot_X.setLayer(layer)
        self.barplot_Y.setLayer(layer)
        self.barplot_color_field.setLayer(layer)


    def plot(self, ax):
        layer = self.barplot_layer.currentLayer()

        X_field_name = self.barplot_X.currentField()
        Y_field_name = self.barplot_Y.currentField()
        color_field_name = self.barplot_color_field.currentField()
        fields = [X_field_name, Y_field_name]
        if color_field_name:
            fields.append(color_field_name)

        df = vector_layer_to_df(layer, *fields)

        if color_field_name:
            check_colors(df[color_field_name], 10)

        sns.barplot(
            data=df,
            x=X_field_name,
            y=Y_field_name,
            hue=color_field_name if color_field_name else None,
            color=self.barplot_color.color().getRgbF(),
            alpha=self.barplot_opacity.opacity(),
            estimator=self.barplot_estimator.currentText().lower(),
            errorbar=('ci', 95) if str_to_bool(self.barplot_errorbars) else None,
            ax=ax
        )


    def plot_example(self, ax):
        penguins = sns.load_dataset("penguins")

        sns.barplot(
            data=penguins,
            x="flipper_length_mm",
            y="species",
            hue="species",
            palette="dark",
            ax=ax
        )


    def reset(self):
        pass
