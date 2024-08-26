from typing import Any, Dict

from qgis.gui import QgsDoubleSpinBox, QgsSpinBox
from qgis.PyQt.QtWidgets import QCheckBox, QComboBox, QLabel, QLineEdit

from eis_qgis_plugin.wizard.modeling.machine_learning.ml_model_main import EISMLModel
from eis_qgis_plugin.wizard.modeling.model_utils import ModelKind


class EISWizardMLP(EISMLModel):
    """
    Class for MLP models.
    """

    def __init__(self, parent, model_kind) -> None:
        self.model_kind = model_kind
        self.model_type = "MLP " + ("classifier" if model_kind == ModelKind.CLASSIFIER else "regressor")

        super().__init__(parent, self.model_type, self.model_kind)
        
        self.training_tab = super().get_training_tab()
        self.training_tab.add_common_parameters()
        self.add_model_parameters()

        if model_kind == ModelKind.CLASSIFIER:
            self.initialize_classifier()
        elif model_kind == ModelKind.REGRESSOR:
            self.initialize_regressor()


    def add_model_parameters(self):
        """Add parameter widgets for MLP model."""
        self.neurons_label = QLabel()
        self.neurons_label.setText("Neurons")
        self.neurons = QLineEdit()
        self.training_tab.add_parameter_row(self.neurons_label, self.neurons)

        self.output_neurons_label = QLabel()
        self.output_neurons_label.setText("Output neurons")
        self.output_neurons = QgsSpinBox()
        self.output_neurons.setMinimum(1)
        self.output_neurons.setValue(1)
        self.training_tab.add_parameter_row(self.output_neurons_label, self.output_neurons)

        self.activation_label = QLabel()
        self.activation_label.setText("Activation")
        self.activation = QComboBox()
        self.activation.addItems(["relu", "linear", "sigmoid", "tanh"])
        self.training_tab.add_parameter_row(self.activation_label, self.activation)

        self.last_activation_label = QLabel()
        self.last_activation_label.setText("Last activation")
        self.last_activation = QComboBox()
        self.training_tab.add_parameter_row(self.last_activation_label, self.last_activation)

        self.epcohs_label = QLabel()
        self.epcohs_label.setText("Epochs")
        self.epcohs = QgsSpinBox()
        self.epcohs.setMinimum(1)
        self.epcohs.setValue(50)
        self.training_tab.add_parameter_row(self.epcohs_label, self.epcohs)

        self.batch_size_label = QLabel()
        self.batch_size_label.setText("Batch size")
        self.batch_size = QgsSpinBox()
        self.batch_size.setMinimum(1)
        self.batch_size.setValue(32)
        self.training_tab.add_parameter_row(self.batch_size_label, self.batch_size)

        self.optimizer_label = QLabel()
        self.optimizer_label.setText("Optimizer")
        self.optimizer = QComboBox()
        self.optimizer.addItems(["adam", "adagrad", "rmsprop", "sdg"])
        self.training_tab.add_parameter_row(self.optimizer_label, self.optimizer)

        self.learning_rate_label = QLabel()
        self.learning_rate_label.setText("Learning rate")
        self.learning_rate = QgsDoubleSpinBox()
        self.learning_rate.setMinimum(0.0001)
        self.learning_rate.setValue(0.001)
        self.learning_rate.setDecimals(5)
        self.training_tab.add_parameter_row(self.learning_rate_label, self.learning_rate)

        self.loss_function_label = QLabel()
        self.loss_function_label.setText("Loss function")
        self.loss_function = QComboBox()
        self.training_tab.add_parameter_row(self.loss_function_label, self.loss_function)

        self.dropout_rate_label = QLabel()
        self.dropout_rate_label.setText("Dropout rate")
        self.dropout_rate = QgsDoubleSpinBox()
        self.dropout_rate.setMinimum(0.0)
        self.dropout_rate.setMaximum(1.0)
        self.dropout_rate.setDecimals(5)
        self.training_tab.add_parameter_row(self.dropout_rate_label, self.dropout_rate)

        self.early_stopping_label = QLabel()
        self.early_stopping_label.setText("Early stopping")
        self.early_stopping = QCheckBox()
        self.early_stopping.setChecked(True)
        self.training_tab.add_parameter_row(self.early_stopping_label, self.early_stopping)

        self.es_patience_label = QLabel()
        self.es_patience_label.setText("Early stopping patience")
        self.es_patience = QgsSpinBox()
        self.es_patience.setMinimum(1)
        self.es_patience.setValue(5)
        self.training_tab.add_parameter_row(self.es_patience_label, self.es_patience)


    def initialize_classifier(self):
        """Initialize MLP classifier settings."""
        self.name = "MLP classifier"
        self.alg_name = "eis:mlp_classifier_train"
        self.last_activation.addItems(["sigmoid", "softmax"])
        self.loss_function.addItems(["binary_crossentropy", "categorical_crossentropy"])
        
        # Customize validation metrics for MLP classifier (no R2 for now)
        self.training_tab.validation_metrics.clear()
        self.training_tab.validation_metrics.addItems(["accuracy", "precision", "recall"])


    def initialize_regressor(self):
        """Initialize MLP egressor settings."""
        self.name = "MLP regressor"
        self.alg_name = "eis:mlp_regressor_train"
        self.last_activation.addItems(["linear"])
        self.loss_function.addItems(["mse", "mae", "hinge", "huber"])


    def get_parameter_values(self, as_str: bool = False) -> Dict[str, Any]:
        return {
            'n_estimators': self.n_estimators.value(),
            'criterion': self.criterion.currentText() if as_str else self.criterion.currentIndex(),
            'max_depth': self.max_depth.value()
        }


    def reset_parameters(self):
        """Reset random forest parameters to defaults."""
        self.training_tab.reset_parameters()

        #TODO
        pass
        # self.n_estimators.setValue(100)
        # self.criterion.setCurrentIndex(0)
        # self.max_depth.setValue(-1)


    def set_tooltips(self):
        """Set tooltips for random forest parameters."""
        self.training_tab.set_tooltips()

        #TODO
        pass

        # n_estimators_tip = "The number of trees in the forest."
        # self.n_estimators.setToolTip(n_estimators_tip)
        # self.n_estimators_label.setToolTip(n_estimators_tip)

        # criterion_tip = "" # TODO
        # self.criterion.setToolTip(criterion_tip)
        # self.criterion_label.setToolTip(criterion_tip)

        # max_depth_tip = (
        #     "The maximum depth of the tree. If None, nodes are expanded until all leaves are pure or"
        #     " until all leaves contain less than min_samples_split samples."
        # )
        # self.max_depth.setToolTip(max_depth_tip)
        # self.max_depth_label.setToolTip(max_depth_tip)


