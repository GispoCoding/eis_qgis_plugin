import numpy as np
import pandas as pd
from qgis.core import Qgis, QgsMapLayer, QgsRasterLayer, QgsVectorLayer
from qgis.gui import QgsCollapsibleGroupBox, QgsColorButton, QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import QSizePolicy, QWidget

from eis_qgis_plugin.wizard.utils.settings_manager import EISSettingsManager


class EISPlot(QWidget):
    """Template / parent class for plot classes in EIS Wizard."""

    def __init__(self, parent) -> None:

        # DELCARE TYPES
        self.layer: QgsMapLayerComboBox
        self.parameter_box: QgsCollapsibleGroupBox
        self.color: QgsColorButton
        self.collapsed_height: int

        # Initialize
        super().__init__(parent)
        self.setupUi(self)

        self.original_height = self.height()

        # Connect layer change updates and populate initial layer
        self.layer.layerChanged.connect(self.update_layer)
        self.update_layer(self.layer.currentLayer())

        # Save original widget size and connect groupbox collapse signal to resizing
        self.parameter_box.collapsedStateChanged.connect(self.resize_parameter_box)

        self.reset()

    def update_layer(self, layer: QgsMapLayer):
        """Update widgets when layer is changed. Should be implemented in the child class."""
        raise NotImplementedError("Update layer needs to be defined in child class.")

    def plot(self, ax):
        """Plot. Should be implemented in the child class."""
        raise NotImplementedError("Plot needs to be defined in child class.")

    def reset(self):
        """Reset plot parameters to defaults."""
        self.parameter_box.setCollapsed(False)

        if hasattr(self, 'color'):
            self.set_deafult_color()

    def set_deafult_color(self):
        """Fetch default color from settings and set color widget selection."""
        self.color.setColor(EISSettingsManager.get_default_color())

    @staticmethod
    def get_default_categorical_palette() -> str:
        return EISSettingsManager.get_default_categorical_palette()

    @staticmethod
    def get_default_continuous_palette() -> str:
        return EISSettingsManager.get_default_continuous_palette()

    def resize_parameter_box(self, collapsed: bool):
        """Resize self and the parent widget (QStackedWidget) according to collapse signal."""
        if collapsed:
            self.setMinimumHeight(self.collapsed_height)
            self.setMaximumHeight(self.collapsed_height)
        else:
            self.setMinimumHeight(self.original_height)
            self.setMaximumHeight(self.original_height)
        container = self.parentWidget()
        container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        container.setMinimumHeight(self.height())
        # container.setMaximumHeight(self.height())

    @staticmethod
    def check_unique_values(df: pd.DataFrame, field_name: str, threshold: int = 10):
        """
        Check if given field in a Dataframe has more unique values than given threshold.

        Can be used for input validation for SNS hues, style and size parameters (or other
        field inputs that expect categorical data).
        """
        values = df[field_name]
        nr_of_values = np.unique(values).size
        if nr_of_values > threshold:
            raise Exception(f"Too many unique values in selected {field_name}. ({values} > {threshold})")

    @staticmethod
    def str_to_bool(str: str) -> bool:
        """Conversion from str to bool."""
        return bool(str.lower() == "true")

    @staticmethod
    def convert_dtype(qgis_dtype) -> np.dtype:
        """Convert QGIS datatype to Numpy type."""
        if qgis_dtype == Qgis.Float32:
            dtype = np.float32
        elif qgis_dtype == Qgis.Float64:
            dtype = np.float64
        elif qgis_dtype == Qgis.Int16:
            dtype = np.int16
        elif qgis_dtype == Qgis.Int32:
            dtype = np.int32
        elif qgis_dtype == Qgis.UInt16:
            dtype = np.uint16
        elif qgis_dtype == Qgis.UInt32:
            dtype = np.uint32
        else:
            raise Exception(f"Datatype conversion to Numpy failed. Raster dtype: {qgis_dtype}")

        return dtype
    
    @staticmethod
    def vector_layer_to_numpy(layer: QgsVectorLayer, *fields):
        data = np.array([
            [feature[field] for field in fields]
            for feature in layer.getFeatures()
        ])
        return data

    @staticmethod
    def vector_layer_to_df(layer: QgsVectorLayer, *fields) -> pd.DataFrame:
        """Create a DataFrame from given vector layer and its fields."""
        nr_of_features = layer.featureCount()

        df_data = {}
        for field in fields:
            df_data[field] = np.empty(nr_of_features)

        # Iterate over features and collect to arrays
        for i, feature in enumerate(layer.getFeatures()):
            for field in fields:
                df_data[field][i] = feature[field]

        # Create a DataFrame
        df = pd.DataFrame(df_data)

        return df

    @staticmethod
    def raster_layer_to_array(layer: QgsRasterLayer, filter_nodata: bool = True) -> np.ndarray:
        """Create a 1D Numpy array from raster layer and filter nodata."""
        provider = layer.dataProvider()
        rows, cols = layer.height(), layer.width()

        block = provider.block(1, layer.extent(), cols, rows)
        numpy_dtype = EISPlot.convert_dtype(block.dataType())
        data = np.frombuffer(block.data(), dtype=numpy_dtype)

        if filter_nodata:
            filtered_data = data[data != block.noDataValue()]
            return filtered_data

        return data
