import seaborn as sns
from qgis.gui import QgsFieldComboBox, QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import QComboBox, QListWidget, QPushButton, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.plots.plot_template import EISPlot

FORM_CLASS: QWidget = load_ui("wizard_plot_pairplot.ui")

KIND_MAPPING = {"histogram": "hist", "scatterplot": "scatter", "kde": "kde", "regression": "reg"}
DIAG_KIND_MAPPING = {"auto": "auto", "histogram": "hist", "kde": "kde", "none": "None"}


class EISWizardPairplot(EISPlot, FORM_CLASS):
    """
    Class for EIS-Seaborn pairplots.

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    layer: QgsMapLayerComboBox
    fields: QListWidget

    color_field: QgsFieldComboBox
    kind: QComboBox
    diagonal_kind: QComboBox

    select_all_btn: QPushButton
    deselect_all_btn: QPushButton


    def __init__(self, parent=None) -> None:
        self.collapsed_height = 270

        super().__init__(parent)

        self.select_all_btn.clicked.connect(self.fields.selectAll)
        self.deselect_all_btn.clicked.connect(self.fields.clearSelection)


    def update_layer(self, layer):
        """Update (set/add items) widgets based on selected layer."""
        if layer is None:
            return

        self.fields.addItems(field.name() for field in layer.fields())
        self.color_field.setLayer(layer)


    def plot(self, ax):
        """Plot to given axis."""
        layer = self.layer.currentLayer()

        fields = [item.text() for item in self.fields.selectedItems()]
        color_field_name = self.color_field.currentField()
        if color_field_name:
            fields.append(color_field_name)

        df = self.vector_layer_to_df(layer, *fields)

        if color_field_name:
            self.check_unique_values(df, color_field_name, 10)

        grid = sns.pairplot(
            data=df,
            hue=color_field_name if color_field_name else None,
            kind=KIND_MAPPING[self.kind.currentText().lower()],
            diag_kind=DIAG_KIND_MAPPING[self.diagonal_kind.currentText().lower()]
        )

        return grid.figure


    def plot_example(self, ax):
        """Produce example plot using SNS data."""
        penguins = sns.load_dataset("penguins")

        grid = sns.pairplot(
            data=penguins,
            hue="species",
            palette="dark",
        )

        return grid.figure


    def reset(self):
        """Reset parameters to defaults."""
        super().reset()

        self.color_field.setField("")
        self.kind.setCurrentIndex(0)
        self.diagonal_kind.setCurrentIndex(0)