import seaborn as sns
from qgis.core import QgsMapLayerProxyModel
from qgis.gui import QgsColorButton, QgsFieldComboBox, QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import QComboBox, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.plots.utils import check_colors, vector_layer_to_df

FORM_CLASS: QWidget = load_ui("wizard_plot_boxplot.ui")


class EISWizardBoxplot(QWidget, FORM_CLASS):

    boxplot_layer: QgsMapLayerComboBox
    boxplot_X: QgsFieldComboBox
    boxplot_Y: QgsFieldComboBox

    boxplot_color_field: QgsFieldComboBox
    boxplot_color: QgsColorButton
    boxplot_log_scale: QComboBox
    boxplot_fill: QComboBox


    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.boxplot_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)

        self.boxplot_layer.layerChanged.connect(self.update_layer)
        self.update_layer(self.boxplot_layer.currentLayer())

        # Defaults from settings
        settings = self.parent().parent().settings_page
        self.boxplot_color.setColor(settings.get_default_color())


    def update_layer(self, layer):
        if layer is None:
            return

        self.boxplot_X.setLayer(layer)
        self.boxplot_Y.setLayer(layer)
        self.boxplot_color_field.setLayer(layer)


    def plot(self, ax):
        layer = self.boxplot_layer.currentLayer()

        X_field_name = self.boxplot_X.currentField()
        Y_field_name = self.boxplot_Y.currentField()
        color_field_name = self.boxplot_color_field.currentField()
        fields = [X_field_name, Y_field_name]
        if color_field_name:
            fields.append(color_field_name)

        df = vector_layer_to_df(layer, *fields)

        if color_field_name:
            check_colors(df[color_field_name], 10)

        sns.boxplot(
            data=df,
            x=X_field_name,
            y=Y_field_name,
            hue=color_field_name if color_field_name else None,
            color=self.boxplot_color.color().getRgbF(),
            ax=ax
        )


    def plot_example(self, ax):
        penguins = sns.load_dataset("penguins")

        sns.boxplot(
            data=penguins,
            x="flipper_length_mm",
            y="species",
            hue="species",
            palette="dark",
            ax=ax
        )


    def reset(self):
        pass
