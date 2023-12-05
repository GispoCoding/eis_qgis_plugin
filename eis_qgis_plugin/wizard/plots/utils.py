from typing import Sequence

import numpy as np
import pandas as pd
from qgis.core import Qgis, QgsRasterLayer, QgsVectorLayer


def check_colors(hues: Sequence, threshold: int = 10):
    nr_of_hues = np.unique(hues).size
    if nr_of_hues > threshold:
        raise Exception(f"Too many unique values in selected color field. ({nr_of_hues} > {threshold})")


def str_to_bool(str: str) -> bool:
    return bool(str.lower() == "true")


def convert_dtype(qgis_dtype) -> np.dtype:
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


def vector_layer_to_df(layer: QgsVectorLayer, *fields) -> pd.DataFrame:
    nr_of_features = layer.featureCount()

    print(fields)
    df_data = {}
    for field in fields:
        df_data[field] = np.empty(nr_of_features)

    # Iterate over features and collect to arrays
    for i, feature in enumerate(layer.getFeatures()):
        for field in fields:
            df_data[field][i] = feature[field]

    # Create a DataFrame
    df = pd.DataFrame(df_data)

    # Check if DataFrame is empty
    if df.empty:
        print("No data to plot.")
        return

    return df


def raster_layer_to_array(layer: QgsRasterLayer, filter_nodata: bool = True) -> np.ndarray:
    provider = layer.dataProvider()
    rows, cols = layer.height(), layer.width()

    block = provider.block(1, layer.extent(), cols, rows)
    numpy_dtype = convert_dtype(block.dataType())
    data = np.frombuffer(block.data(), dtype=numpy_dtype)

    if filter_nodata:
        filtered_data = data[data != block.noDataValue()]
        return filtered_data

    return data
