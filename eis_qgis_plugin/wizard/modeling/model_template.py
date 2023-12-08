import numpy as np
import pandas as pd
from qgis.core import Qgis, QgsRasterLayer, QgsVectorLayer
from qgis.PyQt.QtWidgets import QWidget


class EISModel(QWidget):
    """Parent class for model classes in EIS Wizard."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.original_height = self.height()

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
        numpy_dtype = EISModel.convert_dtype(block.dataType())
        data = np.frombuffer(block.data(), dtype=numpy_dtype)

        if filter_nodata:
            filtered_data = data[data != block.noDataValue()]
            return filtered_data

        return data
