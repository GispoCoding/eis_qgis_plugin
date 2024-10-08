from typing import List, Tuple

import matplotlib.colors as mcolors
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import rasterio.profiles
from matplotlib.cm import ScalarMappable
from matplotlib.path import Path
from qgis.core import QgsMapLayerProxyModel, QgsRasterLayer
from qgis.gui import QgsColorButton, QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import QComboBox, QGroupBox, QSizePolicy, QWidget
from qgis.utils import iface

import eis_qgis_plugin.libs.seaborn as sns
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.layer_data_table import LayerDataTable
from eis_qgis_plugin.utils.misc_utils import check_raster_grids
from eis_qgis_plugin.wizard.eda.plots.plot_template import EISPlot

FORM_CLASS: QWidget = load_ui("eda/wizard_plot_parallel_coordinates_raster.ui")


class EISWizardParallelCoordinatesRasterPlot(EISPlot, FORM_CLASS):
    """
    Class for EIS parallel coordinate plots.

    Initialized from a UI file. Responsible for updating widgets and
    producing the plot.
    """

    def __init__(self, parent=None) -> None:
        
        # DECLARE TYPES
        self.data_box: QGroupBox

        self.color_selection: QgsMapLayerComboBox
        self.color_field_type: QComboBox
        self.line_type: QComboBox
        self.color: QgsColorButton

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


    def reset(self):
        """Reset parameters to defaults."""
        super().reset()
        self.color_selection.setCurrentIndex(0)
        self.color_field_type.setCurrentIndex(0)
        self.line_type.setCurrentIndex(0)


    def get_layers(self) -> List[QgsRasterLayer]:
        return [
            self.data_layer_table.cellWidget(row, 0).currentLayer() for row in range(self.data_layer_table.rowCount())
        ]


    def plot(self, ax, fig):
        # 1 Prepare and check data
        data, field_names, y_min, y_max = self.prepare_data()

        color_data, color_labels, color_field_type, cmap, norm = self.prepare_color_data()
        if not self.perform_checks(field_names, color_data, color_field_type):
            return

        # 2 Prepare plot
        self.prepare_plot(ax, data, y_min, y_max, field_names)
        if color_data is not None:
            self.prepare_legend(ax, color_data, color_labels, color_field_type, cmap, norm)

        # 3 Draw
        self.draw(ax, data, color_data, cmap, norm)


    def perform_checks(self, fields, color_data, color_field_type) -> bool:
        ok = True
        if len(fields) > 15:
            iface.messageBar().pushCritical("Error: ", "Cannot select more than 15 fields.")
            ok = False
        n_categories = len(np.unique(color_data))
        if n_categories > 15 and color_field_type == "categorical":
            iface.messageBar().pushCritical(
                "Error: ",
                f"Categorical color column can have at most 15 unique values, {n_categories} categories detected."
            )
            ok = False
        return ok
    

    def prepare_data(self):
        # Get input values
        rasters = self.get_layers()
        raster_names = [raster.name() for raster in rasters]

        raster_profiles = []
        for raster in rasters:
            path = raster.dataProvider().dataSourceUri()
            with rasterio.open(path) as r:
                raster_profiles.append(r.profile)

        check_raster_grids(raster_profiles)
            
        # Get data as Numpy array
        height = rasters[0].height()
        width = rasters[0].width()
        raster_data = np.empty((height * width, 0), dtype=np.float32)
        for raster in rasters:
            data = self.raster_layer_to_array(raster)
            raster_data = np.hstack((raster_data, data.reshape(-1, 1)))
        data, y_min, y_max = self._normalize_data(raster_data)

        return data, raster_names, y_min, y_max


    def _normalize_data(self, data: np.ndarray) -> Tuple[np.ndarray, float, float]:
        y_min = np.nanmin(data, axis=0)
        y_max = np.nanmax(data, axis=0)
        dy = y_max - y_min
        y_min -= dy * 0.05
        y_max += dy * 0.05
        dy = y_max - y_min

        normalized_data = np.zeros_like(data)
        normalized_data[:, 0] = data[:, 0]
        normalized_data[:, 1:] = (data[:, 1:] - y_min[1:]) / dy[1:] * dy[0] + y_min[0]

        return normalized_data, y_min, y_max


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


    def _encode_data(self, color_data: list) -> np.ndarray:
        unique_values = list(dict.fromkeys(color_data))
        encoding = {value: i for i, value in enumerate(unique_values)}
        color_data_encoded = [encoding[value] for value in color_data]
        return unique_values, color_data_encoded


    def prepare_plot(self, ax, data, y_min, y_max, data_labels):
        axes_list = [ax] + [ax.twinx() for _ in range(data.shape[1] - 1)]
        for i, axis in enumerate(axes_list):
            axis.set_ylim(y_min[i], y_max[i])
            axis.spines["top"].set_visible(False)
            axis.spines["bottom"].set_visible(False)
            if axis != ax:
                axis.spines["right"].set_visible(False)
                axis.yaxis.set_ticks_position("left")
                axis.spines["left"].set_position(("axes", i / (data.shape[1] - 1)))

        ax.set_xlim(0, data.shape[1] - 1)
        ax.set_xticks(range(data.shape[1]))
        ax.set_xticklabels(data_labels, fontsize=10)
        ax.tick_params(axis="x", which="major", pad=7)
        ax.spines["right"].set_visible(False)
        ax.xaxis.tick_top()
    

    def prepare_legend(self, ax, color_data, color_labels, color_field_type, cmap, norm):
        color_column_name = self.color_selection.currentLayer().name()
        if color_field_type == "categorical":
            # Create legend for categorical color data
            legend_handles = [
                patches.Patch(color=cmap(norm(i)), label=category) for i, category in enumerate(color_labels)
            ]
            ax.legend(handles=legend_handles, title=color_column_name, bbox_to_anchor=(1.05, 1), loc='upper left')
        else:
            # Create colorbar for continuous color data
            scalar_mappable = ScalarMappable(norm=norm, cmap=cmap)
            scalar_mappable.set_array(color_data)
            colorbar = plt.colorbar(scalar_mappable, ax=ax, orientation='vertical')
            colorbar.set_label(color_column_name)

            # scalar_mappable = ScalarMappable(norm=norm, cmap=cmap)
            # scalar_mappable.set_array(color_data)  # Use original color data here
            # colorbar = fig.colorbar(scalar_mappable, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
            # colorbar.set_label(color_column_name)
            # colorbar.set_ticks([norm(color_min), norm(color_max)])
            # colorbar.set_ticklabels([f"{color_min:.2f}", f"{color_max:.2f}"])

            # divider = make_axes_locatable(ax)
            # cax = divider.append_axes("right", size="5%", pad=0.25)

            # # Create and display the colorbar in the newly added axes
            # scalar_mappable = ScalarMappable(norm=norm, cmap=cmap)
            # scalar_mappable.set_array([])
            # cbar = plt.colorbar(scalar_mappable, cax=cax)
            # cbar.set_label(color_column_name)
            # cbar.set_ticks([norm(color_min), norm(color_max)])
            # cbar.set_ticklabels([f"{color_min:.2f}", f"{color_max:.2f}"])


    def draw(self, ax, data, color_data, cmap, norm):
        curved_lines = self.line_type.currentIndex() == 0

        for i in range(data.shape[0]):
            if color_data is None:
                color = cmap  # Static color
            else:
                color = cmap(norm(color_data[i]))
            if curved_lines:
                x = np.linspace(0, len(data) - 1, len(data) * 3 - 2, endpoint=True)
                y = np.repeat(data[i, :], 3)[1:-1]

                control_points = list(zip(x, y))
                codes = [Path.MOVETO] + [Path.CURVE4 for _ in range(len(control_points) - 1)]
                path = Path(control_points, codes)

                curve_patch = patches.PathPatch(path, facecolor="none", edgecolor=color, lw=1, alpha=0.5)
                ax.add_patch(curve_patch)
            else:
                ax.plot(range(data.shape[1]), data[i, :], c=color, lw=1, alpha=0.5)

        plt.tight_layout()
