from qgis.core import QgsMapLayerProxyModel
from qgis.gui import (
    QgsColorButton,
    QgsFieldComboBox,
    QgsOpacityWidget,
)
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QWidget,
)

import eis_qgis_plugin.libs.seaborn as sns
from eis_qgis_plugin.eis_wizard.eda.plots.plot_template import EISPlot
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QWidget = load_ui("eda/wizard_plot_barplot.ui")


class EISWizardBarplot(EISPlot, FORM_CLASS):
    """
    Class for EIS-Seaborn barplots.

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    def __init__(self, parent=None) -> None:

        # DECLARE TYPES
        self.X: QgsFieldComboBox
        self.Y: QgsFieldComboBox

        self.color_field: QgsFieldComboBox
        self.color: QgsColorButton
        self.opacity: QgsOpacityWidget
        self.log_scale: QComboBox
        self.estimator: QComboBox
        self.errorbars: QComboBox

        # Initialize
        self.collapsed_height = 200
        super().__init__(parent)
        self.layer.setFilters(QgsMapLayerProxyModel.VectorLayer)

        self.layer.layerChanged.connect(self.update_layer)
        self.update_layer(self.layer.currentLayer())


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

        sns.barplot(
            data=df,
            x=X_field_name,
            y=Y_field_name,
            hue=color_field_name if color_field_name else None,
            color=self.color.color().getRgbF(),
            alpha=self.opacity.opacity(),
            estimator=self.estimator.currentText().lower(),
            errorbar=('ci', 95) if self.str_to_bool(self.errorbars) else None,
            ax=ax
        )


    def plot_example(self, ax):
        """Produce example plot using SNS data."""
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
        """Reset parameters to defaults."""
        super().reset()

        self.color_field.setField("")
        self.opacity.setOpacity(100)
        self.log_scale.setCurrentIndex(0)
        self.estimator.setCurrentIndex(0)
        self.errorbars.setCurrentIndex(0)
