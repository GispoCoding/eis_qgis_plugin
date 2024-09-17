import time
from datetime import date
from os import PathLike
from typing import Any, Dict, Optional, Union

from qgis.core import QgsMapLayer
from qgis.gui import QgsCheckableComboBox, QgsFileWidget, QgsMapLayerComboBox, QgsSpinBox
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QGroupBox,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.ml_model_info import MLModelInfo
from eis_qgis_plugin.wizard.modeling.model_data_table import ModelTrainingDataTable
from eis_qgis_plugin.wizard.utils.algorithm_execution import AlgorithmExecutor
from eis_qgis_plugin.wizard.utils.misc_utils import set_filter
from eis_qgis_plugin.wizard.utils.model_feedback import EISProcessingFeedback

FORM_CLASS: QWidget = load_ui("modeling/training.ui")



class EISMLModelTraining(QWidget, FORM_CLASS):

    def __init__(self, parent, model_main) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.model_main = model_main

        # DECLARE TYPES
        self.train_model_instance_name: QLineEdit
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
        self.validation_metrics: QgsCheckableComboBox

        self.start_training_btn: QPushButton
        self.cancel_training_btn: QPushButton
        self.reset_training_parameters_btn: QPushButton
        self.generate_tags_btn: QPushButton

        self.instance_name_warning_label: QLabel

        self.training_log: QTextEdit
        self.training_progress_bar: QProgressBar

        self.results_table: QTableWidget

        # Initialize
        self.train_evidence_data = ModelTrainingDataTable(self)
        self.train_evidence_data_layout.addWidget(self.train_evidence_data)
        self.training_feedback = EISProcessingFeedback(
            text_edit=self.training_log, progress_bar=self.training_progress_bar
        )
        self.add_validation_metrics()
        self.check_model_instance_name()

        set_filter(self.train_model_save_path, "joblib")

        self.executor = AlgorithmExecutor()
        self.executor.finished.connect(self.on_algorithm_executor_finished)
        self.executor.terminated.connect(self.on_algorithm_executor_terminated)
        self.executor.error.connect(self.on_algorithm_executor_error)

        # Connect signals
        self.validation_method.currentTextChanged.connect(self.update_validation_settings)
        self.start_training_btn.clicked.connect(self.train_model)
        self.cancel_training_btn.clicked.connect(self.cancel)
        self.reset_training_parameters_btn.clicked.connect(self.reset_parameters)
        self.generate_tags_btn.clicked.connect(self.train_evidence_data.generate_tags)
        self.train_model_instance_name.editingFinished.connect(self.check_model_instance_name)


    def add_validation_metrics(self):
        self.validation_metrics.clear()
        metrics = self.model_main.get_valid_metrics()
        self.validation_metrics.addItems(metrics)
        self.validation_metrics.setCheckedItems([metrics[0]])

    # def initialize_classifier(self):
    #     """Initialize general settings of a classifier model."""
    #     self.validation_metrics.clear()
    #     self.validation_metrics.addItems(CLASSIFIER_METRICS)
    #     self.validation_metrics.setCheckedItems([CLASSIFIER_METRICS[0]])


    # def initialize_regressor(self):
    #     """Initialize general settings of a regressor model."""
    #     self.validation_metrics.clear()
    #     self.validation_metrics.addItems(REGRESSOR_METRICS)
    #     self.validation_metrics.setCheckedItems([REGRESSOR_METRICS[0]])


    def on_algorithm_executor_finished(self, result, execution_time):
        if self.training_feedback.no_errors:
            model_parameters_as_str = {
                **self.model_main.get_parameter_values(as_str = True),
                **self.get_common_parameter_values(),
                **self.get_validation_settings(as_str = True)
            }
            self.save_info(model_parameters_as_str, execution_time)
            self.training_feedback.pushInfo(f"\nTraining time: {execution_time}")
        else:
            self.training_feedback.report_failed_run()


    def on_algorithm_executor_error(self, error_message: str):
        self.training_feedback.report_failed_run()


    def on_algorithm_executor_terminated(self):
        self.training_feedback = EISProcessingFeedback(
            text_edit=self.training_log, progress_bar=self.training_progress_bar
        )


    def check_model_instance_name(self):
        if self.model_main.get_model_manager().model_info_exists(self.train_model_instance_name.text()):
            self.instance_name_warning_label.show()
        else:
            self.instance_name_warning_label.hide()


    def add_parameter_row(self, label, widget):
        """Add parameter row to the parameter box layout."""
        self.train_parameter_box.layout().addRow(label, widget)


    def add_common_parameters(self):
        """Add common parameters to the parameter box."""
        self.verbose_label = QLabel()
        self.verbose_label.setText("Verbose")
        self.verbose = QgsSpinBox()
        self.verbose.setMinimum(0)
        self.verbose.setMaximum(2)
        self.add_parameter_row(self.verbose_label, self.verbose)

        self.random_state_label = QLabel()
        self.random_state_label.setText("Random state")
        self.random_state = QgsSpinBox()
        self.random_state.setMinimum(-1)
        self.random_state.setMaximum(10000)
        self.random_state.setValue(-1)
        self.random_state.setSpecialValueText("None (random)")
        self.add_parameter_row(self.random_state_label, self.random_state)


    def update_validation_settings(self, method: str):
        """Change available choices in GUI based on selected validation method."""
        method = method.lower()
        if method == "split":
            self.split_size.setEnabled(True)
            self.cv_folds.setEnabled(False)
            self.validation_metrics.setEnabled(True)
        elif method == "leave-one-out cv":
            self.split_size.setEnabled(False)
            self.cv_folds.setEnabled(False)
            self.validation_metrics.setEnabled(True)
        elif method == "none":
            self.split_size.setEnabled(False)
            self.cv_folds.setEnabled(False)
            self.validation_metrics.setEnabled(False)
        else:
            self.split_size.setEnabled(False)
            self.cv_folds.setEnabled(True)
            self.validation_metrics.setEnabled(True)


    def get_training_label_layer(self) -> QgsMapLayer:
        return self.train_label_data.currentLayer()


    def get_output_file(self) -> Union[str, PathLike]:
        return self.train_model_save_path.filePath()
    

    def get_common_parameter_values(self) -> Dict[str, Any]:
        return {
            "verbose": self.verbose.value(),
            "random_state": None if self.random_state.value() == -1 else self.random_state.value()
        }


    def get_validation_settings(self, as_str: bool = False) -> Dict[str, Any]:
        return {
            "validation_method": self.validation_method.currentText() if
                as_str else self.validation_method.currentIndex(),
            "split_size": self.split_size.value() / 100,
            "cv": self.cv_folds.value(),
            "validation_metrics": self.validation_metrics.checkedItems() if as_str else
                [self.model_main.get_valid_metrics().index(elem) for elem in self.validation_metrics.checkedItems()]
        }


    def check_ready_for_training(self):
        """Check if the inputs are ok to start training process."""
        if self.model_main.model_type == "Logistic regression":
            self.model_main.check_solver_penalties()
        if not self.train_model_instance_name.text():
            raise Exception("No name specified")
        for row in range(self.train_evidence_data.rowCount()):
            tag = self.train_evidence_data.cellWidget(row, 0).text()
            if not tag:
                raise Exception("Tag(s) missing for evidence layers")


    def train_model(self):
        """Trains the ML model. Runs the corresponding processing algorithm."""
        self.check_ready_for_training()

        if self.executor.is_running:
            return

        model_parameters = {
            **self.model_main.get_parameter_values(),
            **self.get_common_parameter_values(),
            **self.get_validation_settings()
        }

        params = {
            "input_rasters": self.train_evidence_data.get_layers(),
            "target_labels": self.get_training_label_layer(),
            "output_file": self.get_output_file(),
            **model_parameters
        }
        self.start_time = time.perf_counter()
        self.executor.configure(self.model_main.get_alg_name(), self.training_feedback)
        self.executor.run(params)


    def cancel(self):
        if self.executor is not None:
            self.executor.cancel()


    def save_info(self, model_parameters: dict, execution_time: Optional[float] = None):
        """Save model info with ModelManager."""
        model_info = MLModelInfo(
            model_instance_name=self.train_model_instance_name.text(),
            model_type=self.model_main.get_model_type(),
            model_kind=self.model_main.get_model_kind(),
            model_file=self.get_output_file(),
            training_date=date.today().strftime("%d.%m.%Y"),
            training_time=execution_time,
            tags=self.train_evidence_data.get_tags(),
            evidence_data=[(layer.name(), layer.source()) for layer in self.train_evidence_data.get_layers()],
            label_data=(self.get_training_label_layer().name(), self.get_training_label_layer().source()),
            parameters=model_parameters,
        )
        self.model_main.get_model_manager().save_model_info(model_info)


    def reset_parameters(self):
        """Reset common and validation parameters to defaults."""
        self.verbose.setValue(0)
        self.random_state.setValue(-1)

        self.validation_method.setCurrentIndex(0)
        self.split_size.setValue(20)
        self.cv_folds.setValue(5)
        self.add_validation_metrics()

        self.model_main.reset_parameters()


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

        validation_metric_tip = "Metrics to use for scoring in validation."
        self.validation_metrics.setToolTip(validation_metric_tip)
        self.validation_metrics_label.setToolTip(validation_metric_tip)
