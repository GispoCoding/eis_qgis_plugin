from qgis.core import QgsMapLayerProxyModel, QgsVectorLayer
from qgis.gui import QgsFieldComboBox
from qgis.PyQt.QtWidgets import QListWidget, QPushButton, QWidget

import eis_qgis_plugin.libs.seaborn as sns
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.eda.plots.pairplot import EISWizardPairplot

FORM_CLASS: QWidget = load_ui("eda/wizard_plot_pairplot_vector.ui")

KIND_MAPPING = {"histogram": "hist", "scatterplot": "scatter", "kde": "kde", "regression": "reg"}
DIAG_KIND_MAPPING = {"auto": "auto", "histogram": "hist", "kde": "kde", "none": "None"}


class EISWizardPairplotVector(EISWizardPairplot, FORM_CLASS):
    """
    Class for EIS-Seaborn pairplots with vector layers.

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    def __init__(self, parent=None) -> None:
        
        # DECLARE TYPES
        self.fields: QListWidget

        self.color_field: QgsFieldComboBox

        self.select_all_btn: QPushButton
        self.deselect_all_btn: QPushButton

        # Initialize
        self.collapsed_height = 270
        super().__init__(parent)

        self.layer.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.select_all_btn.clicked.connect(self.fields.selectAll)
        self.deselect_all_btn.clicked.connect(self.fields.clearSelection)

        self.layer.layerChanged.connect(self.update_layer)
        self.update_layer(self.layer.currentLayer())


    def update_layer(self, layer):
        """Update (set/add items) widgets based on selected layer."""
        if layer is None or not isinstance(layer, QgsVectorLayer):
            return

        self.fields.clear()
        for field in layer.fields():
            if field.isNumeric():
                self.fields.addItem(field.name())

        self.color_field.setLayer(layer)


    def plot(self, ax):
        """Plot to given axis."""
        layer = self.layer.currentLayer()

        fields = [item.text() for item in self.fields.selectedItems()]
        color_field_name = self.color_field.currentField()
        if color_field_name:
            fields.append(color_field_name)

        df = self.vector_layer_to_df(layer, *fields)

        # if color_field_name:
        #     self.check_unique_values(df, color_field_name, 20)

        grid = sns.pairplot(
            data=df,
            hue=color_field_name if color_field_name else None,
            kind=KIND_MAPPING[self.kind.currentText().lower()],
            diag_kind=DIAG_KIND_MAPPING[self.diagonal_kind.currentText().lower()]
        )

        return grid.figure


    def reset(self):
        """Reset parameters to defaults."""
        super().reset()

        self.color_field.setField("")
