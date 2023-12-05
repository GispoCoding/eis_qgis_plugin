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

FORM_CLASS: QWidget = load_ui("wizard_plot_scatterplot.ui")



class EISWizardScatterplot(QWidget, FORM_CLASS):
    """
    Class for EIS-Seaborn scatterplots.

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    scatterplot_layer: QgsMapLayerComboBox
    scatterplot_X: QgsFieldComboBox
    scatterplot_Y: QgsFieldComboBox

    scatterplot_color_field: QgsFieldComboBox
    scatterplot_color: QgsColorButton
    scatterplot_opacity: QgsOpacityWidget
    scatterplot_size: QgsFieldComboBox
    scatterplot_style: QgsFieldComboBox


    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.scatterplot_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)

        self.scatterplot_layer.layerChanged.connect(self.update_layer)
        self.update_layer(self.scatterplot_layer.currentLayer())

        self.settings_page = self.parent().parent().settings_page
        self.reset()

    def _set_deafult_color(self):
        """Fetch default color from settings and set color widget selection."""
        self.scatterplot_color.setColor(self.settings_page.get_default_color())

    def update_layer(self, layer):
        """Update (set) widgets based on selected layer."""
        if layer is None:
            return

        self.scatterplot_X.setLayer(layer)
        self.scatterplot_Y.setLayer(layer)
        self.scatterplot_color_field.setLayer(layer)
        self.scatterplot_size.setLayer(layer)
        self.scatterplot_style.setLayer(layer)


    def plot(self, ax):
        """Plot to given axis."""
        layer = self.scatterplot_layer.currentLayer()

        X_field_name = self.scatterplot_X.currentField()
        Y_field_name = self.scatterplot_Y.currentField()
        color_field_name = self.scatterplot_color_field.currentField()
        size_field_name = self.scatterplot_size.currentField()
        style_field_name = self.scatterplot_style.currentField()
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

        sns.scatterplot(
            data=df,
            x=X_field_name,
            y=Y_field_name,
            hue=color_field_name if color_field_name else None,
            color=self.scatterplot_color.color().getRgbF(),
            alpha=self.scatterplot_opacity.opacity(),
            size=size_field_name if size_field_name else None,
            style=style_field_name if style_field_name else None,
            ax=ax
        )


    def plot_example(self, ax):
        """Produce example plot using SNS data."""
        penguins = sns.load_dataset("penguins")

        sns.scatterplot(
            data=penguins,
            x="flipper_length_mm",
            y="bill_length_mm",
            hue="species",
            palette="dark",
            ax=ax
        )


    def reset(self):
        """Reset parameters to defaults."""
        self.scatterplot_color_field.setField("")
        self._set_deafult_color()
        self.scatterplot_opacity.setOpacity(100)
        self.scatterplot_size.setField("")
        self.scatterplot_style.setField("")
