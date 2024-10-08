
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from qgis.core import QgsMapLayerProxyModel, QgsVectorLayer
from qgis.gui import QgsFieldComboBox
from qgis.PyQt.QtWidgets import QListWidget, QPushButton, QWidget

import eis_qgis_plugin.libs.seaborn as sns
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.eda.plots.parallel_coordinates import EISWizardParallelCoordinatesPlot

FORM_CLASS: QWidget = load_ui("eda/wizard_plot_parallel_coordinates_vector.ui")


class EISWizardParallelCoordinatesVectorPlot(EISWizardParallelCoordinatesPlot, FORM_CLASS):
    """
    Class for EIS parallel coordinate plots.

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    def __init__(self, parent=None) -> None:
        
        self.fields: QListWidget
        self.color_field: QgsFieldComboBox

        self.select_all_btn: QPushButton
        self.deselect_all_btn: QPushButton

        # Initialize
        self.collapsed_height = 270
        super().__init__(parent)
        
        self.dtype = QgsVectorLayer

        self.layer.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.select_all_btn.clicked.connect(self.fields.selectAll)
        self.deselect_all_btn.clicked.connect(self.fields.clearSelection)

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


    def reset(self):
        """Reset parameters to defaults."""
        super().reset()

        self.color_field.setField("")


    def prepare_data(self):
        # Get input values
        layer = self.layer.currentLayer()
        fields = [item.text() for item in self.fields.selectedItems()]

        # Get data as Numpy array
        data = self.vector_layer_to_numpy(layer, *fields, dtype=np.float32)
        data, y_min, y_max = self._normalize_data(data)

        return data, fields, y_min, y_max


    def prepare_color_data(self):
        layer = self.layer.currentLayer()
        color_column_name = self.color_field.currentField()
        if not color_column_name:
            color = self.color.color().getRgbF()
            return None, None, None, color, None
    
        color_field_type = self.color_field_type.currentText().lower()

        if color_field_type == "continuous":
            color_data = np.array(
                [feature[color_column_name] for feature in layer.getFeatures()], dtype=np.float32
            )
            palette_name = self.get_default_continuous_palette()
            color_labels = None

        elif color_field_type == "categorical":
            color_labels, color_data = self._encode_data(
                [feature[color_column_name] for feature in layer.getFeatures()]
            )
            palette_name = self.get_default_categorical_palette()

        else:
            raise ValueError(f"Unknown color field type: {color_field_type}")

        norm = plt.Normalize(np.min(color_data), np.max(color_data))
        cmap = sns.color_palette(palette_name, as_cmap=True)
        if isinstance(cmap, list):
            colors = cmap[:len(set(color_data))]  # Take the first N colors
            cmap = mcolors.LinearSegmentedColormap.from_list("custom_colormap", colors)

        return color_data, color_labels, color_field_type, cmap, norm
