from enum import Enum
from typing import Literal

from qgis.gui import QgsFileWidget
from qgis.PyQt.QtWidgets import QLineEdit

TEMPORARY_OUTPUT = 'TEMPORARY_OUTPUT'
CLASSIFIER_METRICS = ["Accuracy", "Precision", "Recall", "F1", "AUC"]
REGRESSOR_METRICS = ["MSE", "RMSE", "MAE"]

FILE_FILTERS = {
    "raster": "GeoTiff files (*.tif *.tiff)",
    "vector": "",
    "joblib": "Joblib files (*.joblib)"
}

class ModelKind(str, Enum):
    CLASSIFIER = "classifier"
    REGRESSOR = "regressor"


def set_placeholder_text(
    file_widget: QgsFileWidget, placeholder_text = "[Save to temporary file]"
) -> bool:
    """Tries to find QLineEdit in a QgsFileWidget and set its placeholder text."""
    line_edit = file_widget.findChild(QLineEdit)
    if line_edit:
        line_edit.setPlaceholderText(placeholder_text)
        return True
    return False


def set_filter(file_widget: QgsFileWidget, filter: Literal["raster", "vector", "joblib"]) -> bool:
    "Tries to set set specified filter to a QgsFileWidget."
    if filter in FILE_FILTERS.keys():
        file_widget.setFilter(FILE_FILTERS[filter])
        return True
    return False


def get_output_path(file_widget: QgsFileWidget) -> str:
    fp = file_widget.filePath()
    return fp if fp != "" else TEMPORARY_OUTPUT
