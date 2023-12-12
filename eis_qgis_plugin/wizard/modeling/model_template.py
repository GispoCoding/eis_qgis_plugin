from enum import Enum

import numpy as np
import pandas as pd
from qgis.core import Qgis, QgsApplication, QgsRasterLayer, QgsVectorLayer
from qgis.gui import QgsCollapsibleGroupBox, QgsFileWidget, QgsMapLayerComboBox, QgsSpinBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QComboBox, QPushButton, QSizePolicy, QTableWidget, QWidget


class ModelType(Enum):
    CLASSIFIER = 1
    REGRESSOR = 2


CLASSIFIER_METRICS = ["Accuracy", "Precision", "Recall", "F1", "AUC"]
REGRESSOR_METRICS = ["MSE", "RMSE", "MAE"]


class EISModel(QWidget):
    """Parent class for model classes in EIS Wizard."""
    # Data inputs
    training_data: QTableWidget
    y: QgsMapLayerComboBox

    # Group boxes
    parameter_box: QgsCollapsibleGroupBox
    validation_box: QgsCollapsibleGroupBox

    # Save path
    model_save_path: QgsFileWidget

    # Validation widgets
    validation_method: QComboBox
    split_size: QgsSpinBox
    cv_folds: QgsSpinBox
    validation_metric: QComboBox

    # Buttons
    start_training_btn: QPushButton
    reset_btn: QPushButton

    # Results
    results_table: QTableWidget

    start_height: int
    parameter_box_collapse_effect: int


    def __init__(self, parent, model_type) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # current_height keeps track of the last real height of this widget (needed because resizing happens
        # when page of stacked widget is changed)
        self.current_height = self.start_height
        self.model_type = model_type              # Classifier or regressor
        self.validation_box_collapse_effect = 139

        # Initialize table for training data
        self.training_data.setColumnWidth(0, 500)
        self.training_data.setColumnWidth(1, 50)
        self.training_data.setColumnWidth(2, 50)
        self.add_row_to_table()

        # Connect signals
        self.parameter_box.collapsedStateChanged.connect(self.resize_parameter_box)
        self.validation_box.collapsedStateChanged.connect(self.resize_validation_box)
        self.validation_method.currentTextChanged.connect(self.update_validation_settings)

        # Initialize widget sizes
        # NOTE: Not sure why the widget gets initialized with vertically too big and we need to reduce it here..
        self.resize_container(-self.validation_box_collapse_effect-self.parameter_box_collapse_effect)


    def initialize_classifier(self):
        """Initialize general settings of a classifier model."""
        self.validation_metric.clear()
        self.validation_metric.addItems(CLASSIFIER_METRICS)


    def initialize_regressor(self):
        """Initialize general settings of a regressor model."""
        self.validation_metric.clear()
        self.validation_metric.addItems(REGRESSOR_METRICS)


    def resize_parameter_box(self, collapsed: bool):
        """Capture collapse signal of parameter box and resize self and parent forcefully."""
        if collapsed:
            self.resize_container(-self.parameter_box_collapse_effect)
        else:
            self.resize_container(self.parameter_box_collapse_effect)


    def resize_validation_box(self, collapsed: bool):
        """Capture collapse signal of validation box and resize self and parent forcefully."""
        if collapsed:
            self.resize_container(-self.validation_box_collapse_effect)
        else:
            self.resize_container(self.validation_box_collapse_effect)


    def resize_container(self, amount: int):
        """Resizes forcefully self and parent by modifying min and max height by given `amount`."""
        self.setMinimumHeight(self.height() + amount)
        self.setMaximumHeight(self.height() + amount)
        self.current_height = self.height()

        container = self.parentWidget()
        container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        container.setMinimumHeight(self.height())


    def update_validation_settings(self, method: str):
        method = method.lower()
        if method == "split":
            self.split_size.setEnabled(True)
            self.cv_folds.setEnabled(False)
        elif method == "none":
            self.split_size.setEnabled(False)
            self.cv_folds.setEnabled(False)
        else:
            self.split_size.setEnabled(False)
            self.cv_folds.setEnabled(True)


    def create_table_buttons(self):
        """Create buttons for a row in the training data table widget."""
        add_row = QPushButton()
        add_row.setIcon(QIcon(QgsApplication.iconPath('symbologyAdd.svg')))
        add_row.setToolTip('Add a row below.')
        remove_row = QPushButton()
        remove_row.setIcon(QIcon(QgsApplication.iconPath('symbologyRemove.svg')))
        remove_row.setToolTip('Remove row.')

        add_row.clicked.connect(self.add_row_to_table)
        remove_row.clicked.connect(self.remove_row)

        return add_row, remove_row


    def add_row_to_table(self):
        """Add a row in the training data table widget."""
        rows = self.training_data.rowCount()
        if rows == -1:
            rows = 0

        selection = self.training_data.selectedIndexes()
        row_index = rows if len(selection) <= 0 else selection[0].row() + 1

        self.training_data.insertRow(row_index)

        layer_widget = QgsMapLayerComboBox()

        add_btn, remove_btn = self.create_table_buttons()

        self.training_data.setCellWidget(row_index, 0, layer_widget)
        self.training_data.setCellWidget(row_index, 1, add_btn)
        self.training_data.setCellWidget(row_index, 2, remove_btn)

        self.training_data.clearSelection()

        self.resize_container(25)


    def remove_row(self):
        """Remove the selected row from the training data table widget."""
        rows = self.training_data.rowCount()
        if rows == 1:
            return
        selection = self.training_data.selectedIndexes()

        self.training_data.clearSelection()
        self.training_data.removeRow(rows - 1 if len(selection) <= 0 else selection[0].row())

        self.resize_container(-25)


    def get_training_layers(self):
        """Get all layers currently selected in the training data table."""
        return [self.training_data.cellWidget(row, 0).currentLayer() for row in range(self.training_data.rowCount())]


    def train_model(self):
        """Run model. Should be implemented in the child class."""
        raise NotImplementedError("Run model needs to be defined in child class.")


    def reset(self):
        """Reset general model parameters and view."""
        self.parameter_box.setCollapsed(False)
        self.validation_box.setCollapsed(False)

        # Validation settings
        self.validation_method.setCurrentIndex(0)
        self.split_size.setValue(20)
        self.cv_folds.setValue(5)
        self.validation_method.setCurrentIndex(0)


    def populate_table(self):
        self.results_table.clear()
        headers = self.metrics.checkedItems()

        self.results_table.setRowCount(1)
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        # TODO: Populate table with train results


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
