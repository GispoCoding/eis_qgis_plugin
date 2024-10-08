from typing import List

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from qgis.core import QgsMapLayerProxyModel, QgsRasterLayer
from qgis.gui import QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import QGroupBox, QSizePolicy, QWidget

import eis_qgis_plugin.libs.seaborn as sns
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.layer_data_table import LayerDataTable
from eis_qgis_plugin.utils.misc_utils import check_raster_grids
from eis_qgis_plugin.wizard.eda.plots.parallel_coordinates import EISWizardParallelCoordinatesPlot

FORM_CLASS: QWidget = load_ui("eda/wizard_plot_parallel_coordinates_raster.ui")


class EISWizardParallelCoordinatesRasterPlot(EISWizardParallelCoordinatesPlot, FORM_CLASS):
    """
    Class for EIS parallel coordinate plots with raster layers.

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    def __init__(self, parent=None) -> None:
        
        # DECLARE TYPES
        self.data_box: QGroupBox
        self.color_selection: QgsMapLayerComboBox

        # Initialize
        self.collapsed_height = 270
        super().__init__(parent)
        
        self.dtype = QgsRasterLayer

        self.data_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.data_layer_table = LayerDataTable(self, dtype=QgsRasterLayer)
        self.data_box.layout().addWidget(self.data_layer_table)

        self.color_selection.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.color_selection.setAllowEmptyLayer(True)
        self.color_selection.setCurrentIndex(0)

        self.data_layer_table.size_changed.connect(self._update_size)

        self.data_layer_table.add_row()


    def _update_size(self, size_change: int):
        self.setMinimumHeight(self.minimumHeight() + size_change)
        self.setMaximumHeight(self.maximumHeight() + size_change)


    def reset(self):
        """Reset parameters to defaults."""
        super().reset()

        self.color_selection.setCurrentIndex(0)


    def get_layers(self) -> List[QgsRasterLayer]:
        return [
            self.data_layer_table.cellWidget(row, 0).currentLayer() for row in range(self.data_layer_table.rowCount())
        ]


    def prepare_data(self):
        # Get input values
        rasters = self.get_layers()
        raster_names = [raster.name() for raster in rasters]

        # Check matching raster CRSs, cell sizes, pixel alignments, and bounds
        check_raster_grids(rasters)
            
        # Get data as Numpy array
        height = rasters[0].height()
        width = rasters[0].width()
        raster_data = np.empty((height * width, 0), dtype=np.float32)
        for raster in rasters:
            data = self.raster_layer_to_array(raster)
            raster_data = np.hstack((raster_data, data.reshape(-1, 1)))
        data, y_min, y_max = self._normalize_data(raster_data)

        return data, raster_names, y_min, y_max


    def prepare_color_data(self):
        if self.color_selection.currentLayer() is None:
            color = self.color.color().getRgbF()
            return None, None, None, color, None
    
        color_field_type = self.color_field_type.currentText().lower()

        if color_field_type == "continuous":
            color_data = self.raster_layer_to_array(self.color_selection.currentLayer()).astype(np.float32)
            palette_name = self.get_default_continuous_palette()
            color_labels = None

        elif color_field_type == "categorical":
            data = self.raster_layer_to_array(self.color_selection.currentLayer()).astype(np.float32)
            color_labels, color_data = self._encode_data(data)
            palette_name = self.get_default_categorical_palette()

        else:
            raise ValueError(f"Unknown color field type: {color_field_type}")

        norm = plt.Normalize(np.min(color_data), np.max(color_data))
        cmap = sns.color_palette(palette_name, as_cmap=True)
        if isinstance(cmap, list):
            colors = cmap[:len(set(color_data))]  # Take the first N colors
            cmap = mcolors.LinearSegmentedColormap.from_list("custom_colormap", colors)

        return color_data, color_labels, color_field_type, cmap, norm
