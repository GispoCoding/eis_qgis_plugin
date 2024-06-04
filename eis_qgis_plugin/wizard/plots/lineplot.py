from qgis.core import QgsMapLayerProxyModel
from qgis.gui import (
    QgsColorButton,
    QgsFieldComboBox,
    QgsOpacityWidget,
)
from qgis.PyQt.QtWidgets import QWidget

import eis_qgis_plugin.libs.seaborn as sns
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.plots.plot_template import EISPlot

FORM_CLASS: QWidget = load_ui("explore/wizard_plot_lineplot.ui")


class EISWizardLineplot(EISPlot, FORM_CLASS):
    """
    Class for EIS-Seaborn lineplots.

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    def __init__(self, parent=None) -> None:

        # DECLARE TYPES
        self.color_field: QgsFieldComboBox
        self.color: QgsColorButton
        self.opacity: QgsOpacityWidget
        self.size: QgsFieldComboBox
        self.style: QgsFieldComboBox

        # Initialize
        self.collapsed_height = 200
        super().__init__(parent)
        self.layer.setFilters(QgsMapLayerProxyModel.VectorLayer)

        self.update_layer(self.layer.currentLayer())


    def update_layer(self, layer):
        """Update (set) widgets based on selected layer."""
        if layer is None:
            return

        self.X.setLayer(layer)
        self.Y.setLayer(layer)
        self.color_field.setLayer(layer)
        self.size.setLayer(layer)
        self.style.setLayer(layer)


    def plot(self, ax):
        """Plot to given axis."""
        layer = self.layer.currentLayer()

        X_field_name = self.X.currentField()
        Y_field_name = self.Y.currentField()
        color_field_name = self.color_field.currentField()
        size_field_name = self.size.currentField()
        style_field_name = self.style.currentField()
        fields = [X_field_name, Y_field_name]
        if color_field_name:
            fields.append(color_field_name)
        if size_field_name:
            fields.append(size_field_name)
        if style_field_name:
            fields.append(style_field_name)

        df = self.vector_layer_to_df(layer, *fields)

        if color_field_name:
            self.check_unique_values(df, color_field_name, 10)

        if size_field_name:
            self.check_unique_values(df, size_field_name, 10)

        if style_field_name:
            self.check_unique_values(df, style_field_name, 10)

        sns.lineplot(
            data=df,
            x=X_field_name,
            y=Y_field_name,
            hue=color_field_name if color_field_name else None,
            color=self.color.color().getRgbF(),
            alpha=self.opacity.opacity(),
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
        super().reset()

        self.color_field.setField("")
        self.opacity.setOpacity(100)
        self.size.setField("")
        self.style.setField("")
