import seaborn as sns
from qgis.core import QgsMapLayerProxyModel
from qgis.gui import (
    QgsColorButton,
    QgsFieldComboBox,
    QgsMapLayerComboBox,
    QgsOpacityWidget,
)
from qgis.PyQt.QtWidgets import QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.plots.utils import check_colors, vector_layer_to_df

FORM_CLASS: QWidget = load_ui("wizard_plot_lineplot.ui")


class EISWizardLineplot(QWidget, FORM_CLASS):
    """
    Class for EIS-Seaborn lineplots.

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    lineplot_layer: QgsMapLayerComboBox
    lineplot_X: QgsFieldComboBox
    lineplot_Y: QgsFieldComboBox

    lineplot_color_field: QgsFieldComboBox
    lineplot_color: QgsColorButton
    lineplot_opacity: QgsOpacityWidget
    lineplot_size: QgsFieldComboBox
    lineplot_style: QgsFieldComboBox


    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.lineplot_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)

        self.lineplot_layer.layerChanged.connect(self.update_layer)
        self.update_layer(self.lineplot_layer.currentLayer())

        self.settings_page = self.parent().parent().settings_page
        self.reset()

    def _set_deafult_color(self):
        """Fetch default color from settings and set color widget selection."""
        self.lineplot_color.setColor(self.settings_page.get_default_color())

    def update_layer(self, layer):
        """Update (set) widgets based on selected layer."""
        if layer is None:
            return

        self.lineplot_X.setLayer(layer)
        self.lineplot_Y.setLayer(layer)
        self.lineplot_color_field.setLayer(layer)
        self.lineplot_size.setLayer(layer)
        self.lineplot_style.setLayer(layer)


    def plot(self, ax):
        """Plot to given axis."""
        layer = self.lineplot_layer.currentLayer()

        X_field_name = self.lineplot_X.currentField()
        Y_field_name = self.lineplot_Y.currentField()
        color_field_name = self.lineplot_color_field.currentField()
        size_field_name = self.lineplot_size.currentField()
        style_field_name = self.lineplot_style.currentField()
        fields = [X_field_name, Y_field_name]
        if color_field_name:
            fields.append(color_field_name)
        if size_field_name:
            fields.append(size_field_name)
        if style_field_name:
            fields.append(style_field_name)

        df = vector_layer_to_df(layer, *fields)

        if color_field_name:
            check_colors(df[color_field_name], 10)

        sns.lineplot(
            data=df,
            x=X_field_name,
            y=Y_field_name,
            hue=color_field_name if color_field_name else None,
            color=self.lineplot_color.color().getRgbF(),
            alpha=self.lineplot_opacity.opacity(),
            size=size_field_name if size_field_name else None,
            style=style_field_name if style_field_name else None,
            ax=ax
        )


    def plot_example(self, ax):
        """Produce example plot using SNS data."""
        penguins = sns.load_dataset("penguins")

        sns.lineplot(
            data=penguins,
            x="flipper_length_mm",
            y="bill_length_mm",
            hue="species",
            palette="dark",
            ax=ax
        )


    def reset(self):
        """Reset parameters to defaults."""
        self.lineplot_color_field.setField("")
        self._set_deafult_color()
        self.lineplot_opacity.setOpacity(100)
        self.lineplot_size.setField("")
        self.lineplot_style.setField("")
