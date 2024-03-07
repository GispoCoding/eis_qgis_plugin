from enum import Enum
from os import PathLike
from typing import Any, Dict, List, Optional, Union

from qgis import processing
from qgis.core import QgsMapLayer, QgsRasterLayer
from qgis.gui import QgsFileWidget, QgsMapLayerComboBox, QgsSpinBox
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.model_data_table import ModelDataTable, ModelTrainingDataTable

FORM_CLASS: QWidget = load_ui("modeling/wizard_ml_model.ui")


class ModelType(Enum):
    CLASSIFIER = 1
    REGRESSOR = 2


CLASSIFIER_METRICS = ["Accuracy", "Precision", "Recall", "F1", "AUC"]
REGRESSOR_METRICS = ["MSE", "RMSE", "MAE"]

ROW_HEIGHT = 26

DATABASE = {
    "rf_classifier_1": {
        "type": "rf_classifier",
        "path": "path_to_joblib_file",
        "evidence_data": {
            "Li_ppm": "path_to_layer",
            "Cu_ppm": "path_to_layer2",
            "Distances to structures": "path",
            "EM": "path",
            "Geophysics 2": "path"
        },
        "labels_data": "path_to_labels_file",
        "parameters_used": {
            "param_name_1": "value",
        },
        "validation_settings": {
            "": ""
        }
    },
    "rf_regressor_3": {
        "type": "rf_regressor",
        "path": "path_to_joblib_file",
        "evidence_data": {
            "EM": "path_to_layer",
            "AEM_QUAD": "path_to_layer2",
            "Li_ppm_interpolated_very_long_tag_yes": "path_to_layer2",
            "Structures": "path_to_layer2",
        },
    },
}


class EISMLModel(QWidget, FORM_CLASS):
    """Parent class for ML model classes in EIS Wizard."""

    def __init__(self, parent, model_type) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # DECLARE TYPES FOR BETTER DEV EXPERIENCE

        self.modeling_tabs: QTabWidget

        # Tab 0 - Model data preparation

        # Tab 1 - Model training
        self.train_model_name: QLineEdit
        self.train_model_save_path: QgsFileWidget
        self.train_evidence_data_layout: QVBoxLayout
        self.train_label_data: QgsMapLayerComboBox

        self.train_evidence_data_box: QGroupBox
        self.train_label_data_box: QGroupBox
        self.train_parameter_box: QGroupBox
        self.train_validation_box: QGroupBox

        self.validation_method: QComboBox
        self.split_size: QgsSpinBox
        self.cv_folds: QgsSpinBox
        self.validation_metric: QComboBox

        self.start_training_btn: QPushButton
        self.reset_training_parameters_btn: QPushButton

        self.results_table: QTableWidget

        # Tab 2 - Model testing
        self.test_model_selection: QComboBox
        self.test_run_name: QLineEdit
        self.test_evidence_data_layout: QVBoxLayout
        self.test_evidence_data_box: QGroupBox
        self.test_label_data_box: QGroupBox
        self.test_metrics_box: QGroupBox
        self.test_reset_btn: QPushButton
        self.test_run_btn: QPushButton

        # Tab 3 - Model application
        self.application_model_selection: QComboBox
        self.application_run_name: QLineEdit
        self.application_evidence_data_layout: QVBoxLayout
        self.application_evidence_data_box: QGroupBox
        self.application_reset_btn: QPushButton
        self.application_run_btn: QPushButton

        self.model_type = model_type  # Classifier or regressor

        self.initialize_model_data_preparation()
        self.initialize_model_training()
        self.initialize_model_testing()
        self.initialize_model_application()

        self.modeling_tabs.currentChanged.connect(self.update_selectable_models)


    def initialize_model_data_preparation(self):
        pass


    def initialize_model_training(self):
        # Create data table and add it
        self.train_evidence_data = ModelTrainingDataTable(self)
        self.train_evidence_data_layout.addWidget(self.train_evidence_data)

        # Set filter to output file
        self.train_model_save_path.setFilter("Joblib files (*.joblib)")

        # Connect signals
        self.validation_method.currentTextChanged.connect(self.update_validation_settings)
        self.start_training_btn.clicked.connect(self.train_model)
        self.reset_training_parameters_btn.clicked.connect(self.reset_parameters)


    def update_selectable_models(self, tab_index: int = None):
        self.application_model_selection.clear()
        self.application_model_selection.addItems(list(DATABASE.keys()))
        self.test_model_selection.clear()
        self.test_model_selection.addItems(list(DATABASE.keys()))


    def update_data_table(self, table: ModelDataTable, model_key: str):
        if model_key in DATABASE.keys():
            tags = list(DATABASE[model_key]["evidence_data"].keys())
            table.load_model(tags)


    def initialize_model_testing(self):
        # Create data table and add it
        self.test_evidence_data = ModelDataTable(self)
        self.test_evidence_data_layout.addWidget(self.test_evidence_data)

        # Connect signals
        self.test_run_btn.clicked.connect(self.test_model)
        self.test_model_selection.currentTextChanged.connect(
            lambda key: self.update_data_table(self.test_evidence_data, key)
        )
        
        # Initialize model selection and table with data for first model
        self.update_selectable_models()
        if self.test_model_selection.count() > 0:
            self.update_data_table(self.test_evidence_data, self.test_model_selection.currentText())


    def initialize_model_application(self):
        # Create data table and add it
        self.application_evidence_data = ModelDataTable(self)
        self.application_evidence_data_layout.addWidget(self.application_evidence_data)

        # Connect signals
        self.application_run_btn.clicked.connect(self.apply_model)
        self.application_model_selection.currentTextChanged.connect(
            lambda key: self.update_data_table(self.application_evidence_data, key)
        )

        # Initialize table with data for first model
        self.update_selectable_models()  # Could be removed, already initialized in initialize_model_testing
        if self.application_model_selection.count() > 0:
            self.update_data_table(self.application_evidence_data, self.application_model_selection.currentText())


    def initialize_classifier(self):
        """Initialize general settings of a classifier model."""
        self.validation_metric.clear()
        self.validation_metric.addItems(CLASSIFIER_METRICS)


    def initialize_regressor(self):
        """Initialize general settings of a regressor model."""
        self.validation_metric.clear()
        self.validation_metric.addItems(REGRESSOR_METRICS)


    def add_general_model_parameters(self):
        self.verbose_label = QLabel()
        self.verbose_label.setText("Verbose")
        self.verbose = QgsSpinBox()
        self.verbose.setMinimum(0)
        self.verbose.setMaximum(1)
        self.train_parameter_box.layout().addRow(self.verbose_label, self.verbose)

        self.random_state_label = QLabel()
        self.random_state_label.setText("Random state")
        self.random_state = QgsSpinBox()
        self.random_state.setMinimum(-1)
        self.random_state.setMaximum(10000)
        self.random_state.setValue(-1)
        self.random_state.setSpecialValueText("None (random)")
        self.train_parameter_box.layout().addRow(self.random_state_label, self.random_state)


    def update_validation_settings(self, method: str):
        """Change available choices in GUI based on selected validation method."""
        method = method.lower()
        if method == "split":
            self.split_size.setEnabled(True)
            self.cv_folds.setEnabled(False)
            self.validation_metric.setEnabled(True)
        elif method == "leave-one-out cv":
            self.split_size.setEnabled(False)
            self.cv_folds.setEnabled(False)
            self.validation_metric.setEnabled(True)
        elif method == "none":
            self.split_size.setEnabled(False)
            self.cv_folds.setEnabled(False)
            self.validation_metric.setEnabled(False)
        else:
            self.split_size.setEnabled(False)
            self.cv_folds.setEnabled(True)
            self.validation_metric.setEnabled(True)


    def get_evidence_layers(self) -> List[QgsRasterLayer]:
        """Get all layers currently selected in the evidence data table."""
        return [
            self.train_evidence_data.cellWidget(row, 1).currentLayer() 
            for row in range(self.train_evidence_data.rowCount())
        ]
    

    def get_evidence_layers_with_tags(self) -> List[str]:
        """Gets evidence layers with tags as dictionary (tags keys, layers values)."""
        table = self.train_evidence_data
        return {
            table.cellWidget(row, 0).text(): table.cellWidget(row, 1).currentLayer()
            for row in range(table.rowCount())
        }


    def get_label_layer(self) -> QgsMapLayer:
        return self.train_label_data.currentLayer()


    def get_output_file(self) -> Union[str, PathLike]:
        return self.train_model_save_path.filePath()
    

    def get_model_name(self) -> str:
        return self.name


    def get_processing_algorithm_name(self) -> str:
        return self.alg_name


    def get_parameter_values(self) -> Dict[str, Any]:
        raise NotImplementedError("'get_parameter_values' needs to be defined in child class.")


    def get_common_parameter_values(self) -> Dict[str, Any]:
        return {
            'verbose': self.verbose.value(),
            'random_state': None if self.random_state.value() == -1 else self.random_state.value()
        }


    def get_validation_settings(self) -> Dict[str, Any]:
        return {
            'validation_method': self.validation_method.currentIndex(),
            'split_size': self.split_size.value() / 100,
            'cv': self.cv_folds.value(),
            'validation_metric': self.validation_metric.currentIndex()
        }


    def save_training_run_to_model_database(self, execution_time: Optional[float] = None):
        training_run_name = self.train_model_name.text()
        DATABASE[training_run_name] = {
            "model_type": self.get_model_name(),
            "file": self.get_output_file(),
            "evidence_data": self.get_evidence_layers_with_tags(),
            "labels_data": self.get_label_layer(),
            "parameters": {
                **self.get_common_parameter_values(),
                **self.get_parameter_values(),
                **self.get_validation_settings()
            },
            "training_execution_time": execution_time
        }


    def check_ready_for_training(self):
        if not self.train_model_name.text():
            raise Exception("No name specified")
        for row in range(self.train_evidence_data.rowCount()):
            tag = self.train_evidence_data.cellWidget(row, 0).text()
            if not tag:
                raise Exception("Tag(s) missing for evidence layers")


    def train_model(self):
        """Trains the ML model. Runs corresponding processing algorithm."""
        self.check_ready_for_training()
        alg_name = self.get_processing_algorithm_name()
        result = processing.run(
            alg_name,
            {
                'input_rasters': self.get_evidence_layers(),
                'target_labels': self.get_label_layer(),
                'output_file': self.get_output_file(),
                **self.get_parameter_values(),
                **self.get_common_parameter_values(),
                **self.get_validation_settings()
            }
        )

        if result:
            self.save_training_run_to_model_database()


    def test_model(self):
        pass


    def apply_model(self):
        pass


    def reset_parameters(self):
        """Reset common and validation parameters to defaults."""
        self.verbose.setValue(0)
        self.random_state.setValue(-1)

        self.validation_method.setCurrentIndex(0)
        self.split_size.setValue(20)
        self.cv_folds.setValue(5)
        self.validation_method.setCurrentIndex(0)


    def set_tooltips(self):
        """Set tooltips for the common and validation parameters."""
        evidence_data_tooltip = "Evidence layers for training the model."
        self.train_evidence_data.setToolTip(evidence_data_tooltip)
        self.train_evidence_data_box.setToolTip(evidence_data_tooltip)

        label_data_tooltip = "Layer with target labels for training."
        self.train_label_data.setToolTip(label_data_tooltip)
        self.train_label_data_box.setToolTip(label_data_tooltip)

        verbose_tip = (
            "Specifies if modeling progress and performance should be printed."
            " 0 doesn't print, values 1 or above will produce prints."
        )
        self.verbose.setToolTip(verbose_tip)
        self.verbose_label.setToolTip(verbose_tip)

        random_state_tip = "Seed for random number generation."
        self.random_state.setToolTip(random_state_tip)
        self.random_state_label.setToolTip(random_state_tip)

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
