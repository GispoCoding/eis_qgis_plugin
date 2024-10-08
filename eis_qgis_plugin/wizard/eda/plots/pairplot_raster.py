from typing import List

import numpy as np
import pandas as pd
from qgis.core import QgsMapLayerProxyModel, QgsRasterLayer
from qgis.gui import QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import QGroupBox, QSizePolicy, QWidget

import eis_qgis_plugin.libs.seaborn as sns
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.layer_data_table import LayerDataTable
from eis_qgis_plugin.utils.misc_utils import check_raster_grids
from eis_qgis_plugin.wizard.eda.plots.plot_template import EISPlot

FORM_CLASS: QWidget = load_ui("eda/wizard_plot_pairplot_raster.ui")

KIND_MAPPING = {"histogram": "hist", "scatterplot": "scatter", "kde": "kde", "regression": "reg"}
DIAG_KIND_MAPPING = {"auto": "auto", "histogram": "hist", "kde": "kde", "none": "None"}

class EISWizardPairplotRaster(EISPlot, FORM_CLASS):
    """
    Class for EIS-Seaborn pairplots with raster layers.

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    def __init__(self, parent=None) -> None:

        # DECLARE TYPES
        self.data_box = QGroupBox

        self.color_selection: QgsMapLayerComboBox
        
        # Initialize
        self.collapsed_height = 270
        super().__init__(parent)

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


    def get_layers(self) -> List[QgsRasterLayer]:
        return [
            self.data_layer_table.cellWidget(row, 0).currentLayer() for row in range(self.data_layer_table.rowCount())
        ]
    

    def plot(self, ax):
        """Plot to given axis."""
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

        color_field = self.color_selection.currentLayer()
        if color_field is not None:
            color_field_name = color_field.name() if color_field is not None else None
        else:
            color_field_name = None


        df = pd.DataFrame(raster_data, columns=raster_names)

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

        self.color_selection.setCurrentIndex(0)