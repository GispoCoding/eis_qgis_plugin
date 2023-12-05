import seaborn as sns
from qgis.gui import QgsFieldComboBox, QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import QComboBox, QListWidget, QPushButton, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.plots.utils import check_colors, vector_layer_to_df

FORM_CLASS: QWidget = load_ui("wizard_plot_pairplot.ui")

KIND_MAPPING = {"histogram": "hist", "scatterplot": "scatter", "kde": "kde", "regression": "reg"}
DIAG_KIND_MAPPING = {"auto": "auto", "histogram": "hist", "kde": "kde", "none": "None"}


class EISWizardPairplot(QWidget, FORM_CLASS):
    """
    Class for EIS-Seaborn pairplots.

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    pairplot_layer: QgsMapLayerComboBox
    pairplot_fields: QListWidget

    pairplot_color_field: QgsFieldComboBox
    pairplot_kind: QComboBox
    pairplot_diagonal_kind: QComboBox

    pairplot_select_all_btn: QPushButton
    pairplot_deselect_all_btn: QPushButton


    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.pairplot_layer.layerChanged.connect(self.update)

        self.pairplot_select_all_btn.clicked.connect(self.pairplot_fields.selectAll)
        self.pairplot_deselect_all_btn.clicked.connect(self.pairplot_fields.clearSelection)

        self.reset()

    def update(self, layer):
        """Update (set/add items) widgets based on selected layer."""
        if layer is None:
            return

        self.pairplot_fields.addItems(field.name() for field in layer.fields())
        self.pairplot_color_field.setLayer(layer)


    def plot(self, ax):
        """Plot to given axis."""
        layer = self.pairplot_layer.currentLayer()

        fields = [item.text() for item in self.pairplot_fields.selectedItems()]
        color_field_name = self.pairplot_color_field.currentField()
        if color_field_name:
            fields.append(color_field_name)

        df = vector_layer_to_df(layer, *fields)

        if color_field_name:
            check_colors(df[color_field_name], 10)

        grid = sns.pairplot(
            data=df,
            hue=color_field_name if color_field_name else None,
            kind=KIND_MAPPING[self.pairplot_kind.currentText().lower()],
            diag_kind=DIAG_KIND_MAPPING[self.pairplot_diagonal_kind.currentText().lower()]
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
        self.pairplot_color_field.setField("")
        self.pairplot_kind.setCurrentIndex(0)
        self.pairplot_diagonal_kind.setCurrentIndex(0)
