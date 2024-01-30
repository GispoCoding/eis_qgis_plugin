from enum import Enum

from qgis.core import QgsApplication
from qgis.gui import QgsCollapsibleGroupBox, QgsFileWidget, QgsMapLayerComboBox, QgsSpinBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QComboBox, QHeaderView, QPushButton, QSizePolicy, QTableWidget, QWidget


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
        self.training_data.setColumnWidth(0, 200)
        self.training_data.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

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

        self.set_tooltips()

    def initialize_classifier(self):
        """Initialize general settings of a classifier model."""
        self.validation_metric.clear()
        self.validation_metric.addItems(CLASSIFIER_METRICS)


    def initialize_regressor(self):
        """Initialize general settings of a regressor model."""
        self.validation_metric.clear()
        self.validation_metric.addItems(REGRESSOR_METRICS)


    def resize_parameter_box(self, collapsed: bool):
        """Capture collapse signal of parameter box and resize self and parent."""
        if collapsed:
            self.resize_container(-self.parameter_box_collapse_effect)
        else:
            self.resize_container(self.parameter_box_collapse_effect)


    def resize_validation_box(self, collapsed: bool):
        """Capture collapse signal of validation box and resize self and parent."""
        if collapsed:
            self.resize_container(-self.validation_box_collapse_effect)
        else:
            self.resize_container(self.validation_box_collapse_effect)


    def resize_container(self, amount: int):
        """
        Resizes self and parent by modifying min and max height by given `amount`.

        Resizes "forcefully", so sets min and max heights and vertical size policy to fixed.
        """
        self.setMinimumHeight(self.height() + amount)
        self.setMaximumHeight(self.height() + amount)
        self.current_height = self.height()

        container = self.parentWidget()
        container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        container.setMinimumHeight(self.height())


    def update_validation_settings(self, method: str):
        """Change available choices in GUI based on selected validation method."""
        method = method.lower()
        if method == "split":
            self.split_size.setEnabled(True)
            self.cv_folds.setEnabled(False)
        elif method == "leave-one-out cv":
            self.split_size.setEnabled(False)
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
        """Start training the model. Should be implemented in the child class."""
        raise NotImplementedError("Train model needs to be defined in child class.")


    def reset(self):
        """Reset validation parameters to defaults and uncollapse group boxes."""
        self.parameter_box.setCollapsed(False)
        self.validation_box.setCollapsed(False)

        # Validation settings
        self.validation_method.setCurrentIndex(0)
        self.split_size.setValue(20)
        self.cv_folds.setValue(5)
        self.validation_method.setCurrentIndex(0)


    def set_tooltips(self):
        """Set tooltips for the validation parameters."""
        training_data_tooltip = "Layers used for training the model."
        self.training_data.setToolTip(training_data_tooltip)
        self.training_data_label.setToolTip(training_data_tooltip)

        y_tooltip = "Layer with target labels for training."
        self.y.setToolTip(y_tooltip)
        self.y_label.setToolTip(y_tooltip)

        validation_method_tip = (
            "Validation method to use. 'split' divides data into two parts, 'kfold_cv'"
            " performs k-fold cross-validation, 'skfold_cv' performs stratified k-fold cross-validation,"
            " 'loo_cv' performs leave-one-out cross-validation and 'none' will not validate model at all"
            " (in this case, all X and y will be used solely for training).")
        self.validation_method.setToolTip(validation_method_tip)
        self.validation_method_label.setToolTip(validation_method_tip)

        split_size_tip = "Fraction of the dataset to be used as validation data (rest is used for training)."
        self.split_size.setToolTip(split_size_tip)
        self.split_size_label.setToolTip(split_size_tip)

        cv_folds_tip = (
            "Number of folds used in cross-validation. Used only when validation_method is 'kfold_cv' or 'skfold_cv'."
        )
        self.cv_folds.setToolTip(cv_folds_tip)
        self.cv_folds_label.setToolTip(cv_folds_tip)

        validation_metric_tip = "Metric to use for scoring the model."
        self.validation_metric.setToolTip(validation_metric_tip)
        self.validation_metric_label.setToolTip(validation_metric_tip)


    def populate_table(self):
        """TBD if this method is needed."""
        self.results_table.clear()
        headers = self.metrics.checkedItems()

        self.results_table.setRowCount(1)
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        # TODO: Populate table with train results
