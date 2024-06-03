from qgis.core import QgsMapLayerProxyModel
from qgis.gui import QgsColorButton, QgsFieldComboBox
from qgis.PyQt.QtWidgets import QComboBox, QWidget

import eis_qgis_plugin.libs.seaborn as sns
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.plots.plot_template import EISPlot

FORM_CLASS: QWidget = load_ui("explore/wizard_plot_boxplot.ui")


class EISWizardBoxplot(EISPlot, FORM_CLASS):
    """
    Class for EIS-Seaborn boxplots.

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    def __init__(self, parent=None) -> None:
        
        # DECLARE TYPES
        self.X: QgsFieldComboBox
        self.Y: QgsFieldComboBox

        self.color_field: QgsFieldComboBox
        self.color: QgsColorButton
        self.log_scale: QComboBox

        # Initialize
        self.collapsed_height = 200
        super().__init__(parent)
        self.layer.setFilters(QgsMapLayerProxyModel.VectorLayer)


    def update_layer(self, layer):
        """Update (set) widgets based on selected layer."""
        if layer is None:
            return

        self.X.setLayer(layer)
        self.Y.setLayer(layer)
        self.color_field.setLayer(layer)


    def plot(self, ax):
        """Plot to given axis."""
        layer = self.layer.currentLayer()

        X_field_name = self.X.currentField()
        Y_field_name = self.Y.currentField()
        color_field_name = self.color_field.currentField()
        fields = [X_field_name, Y_field_name]
        if color_field_name:
            fields.append(color_field_name)

        df = self.vector_layer_to_df(layer, *fields)

        # if color_field_name:
        #     self.check_unique_values(df, color_field_name, 20)

        sns.boxplot(
            data=df,
            x=X_field_name,
            y=Y_field_name,
            hue=color_field_name if color_field_name else None,
            color=self.color.color().getRgbF(),
            ax=ax
        )


    def plot_example(self, ax):
        """Produce example plot using SNS data."""
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
        """Reset parameters to defaults."""
        super().reset()

        self.color_field.setField("")
        self.log_scale.setCurrentIndex(0)
