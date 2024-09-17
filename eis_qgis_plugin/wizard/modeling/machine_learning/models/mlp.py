from typing import Any, Dict

from qgis.gui import QgsDoubleSpinBox, QgsSpinBox
from qgis.PyQt.QtWidgets import QCheckBox, QComboBox, QLabel, QLineEdit

from eis_qgis_plugin.wizard.modeling.machine_learning.ml_model_main import EISMLModel
from eis_qgis_plugin.wizard.utils.misc_utils import ModelKind


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

        self.epochs_label = QLabel()
        self.epochs_label.setText("Epochs")
        self.epochs = QgsSpinBox()
        self.epochs.setMinimum(1)
        self.epochs.setValue(50)
        self.training_tab.add_parameter_row(self.epochs_label, self.epochs)

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
        self.learning_rate.setDecimals(5)
        self.learning_rate.setMinimum(0.0001)
        self.learning_rate.setValue(0.001)
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
        self.dropout_rate.setValue(0.0)
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
        
        # Customized validation metrics for MLP classifier (no R2 for now)
        self.training_tab.validation_metrics.clear()
        self.training_tab.validation_metrics.addItems(["Accuracy", "Precision", "Recall"])
        self.training_tab.validation_metrics.setCheckedItems(["Accuracy"])


    def initialize_regressor(self):
        """Initialize MLP egressor settings."""
        self.name = "MLP regressor"
        self.alg_name = "eis:mlp_regressor_train"
        self.last_activation.addItems(["linear"])
        self.loss_function.addItems(["mse", "mae", "hinge", "huber"])


    def get_parameter_values(self, as_str: bool = False) -> Dict[str, Any]:
        return {
            "neurons": self.neurons.text(),
            "output_neurons": self.output_neurons.value(),
            "activation": self.activation.currentText() if as_str else self.activation.currentIndex(),
            "last_activation": self.last_activation.currentText() if as_str else self.last_activation.currentIndex(),
            "epochs": self.epochs.value(),
            "batch_size": self.batch_size.value(),
            "optimizer": self.optimizer.currentText() if as_str else self.optimizer.currentIndex(),
            "learning_rate": self.learning_rate.value(),
            "loss_function": self.loss_function.currentText() if as_str else self.loss_function.currentIndex(),
            "dropout_rate": self.dropout_rate.value(),
            "early_stopping": self.early_stopping.isChecked(),
            "es_patience": self.es_patience.value()
        }


    def reset_parameters(self):
        """Reset MLP parameters to defaults."""        
        self.neurons.clear()
        self.output_neurons.setValue(1)
        self.activation.setCurrentIndex(0)
        self.last_activation.setCurrentIndex(0)
        self.epochs.setValue(50)
        self.batch_size.setValue(32)
        self.optimizer.setCurrentIndex(0)
        self.learning_rate.setValue(0.001)
        self.loss_function.setCurrentIndex(0)
        self.dropout_rate.setValue(0.0)
        self.early_stopping.setChecked(True)
        self.es_patience.setValue(5)


    def set_tooltips(self):
        """Set tooltips for random forest parameters."""
        self.training_tab.set_tooltips()

        neurons_tip = "Number of neurons in each hidden layer. Input the neurons as a comma-separated list. \
            For example: 10, 5, 10."
        self.neurons_label.setToolTip(neurons_tip)
        self.neurons.setToolTip(neurons_tip)
        
        output_neurons_tip = "Number of neurons in the output layer."
        self.output_neurons_label.setToolTip(output_neurons_tip)
        self.output_neurons.setToolTip(output_neurons_tip)

        activation_tip = "Activation function used in each hidden layer."
        self.activation_label.setToolTip(activation_tip)
        self.activation.setToolTip(activation_tip)

        last_activation_tip = "Activation function used in the output layer."
        self.last_activation_label.setToolTip(last_activation_tip)
        self.last_activation.setToolTip(last_activation_tip)

        epochs_tip = "Number of epochs to train the model."
        self.epochs_label.setToolTip(epochs_tip)
        self.epochs.setToolTip(epochs_tip)

        batch_size_tip = "Number of samples per gradient update."
        self.batch_size_label.setToolTip(batch_size_tip)
        self.batch_size.setToolTip(batch_size_tip)

        optimizer_tip = "Optimizer to be used."
        self.optimizer_label.setToolTip(optimizer_tip)
        self.optimizer.setToolTip(optimizer_tip)

        learning_rate_tip = "Learning rate to be used in training."
        self.learning_rate_label.setToolTip(learning_rate_tip)
        self.learning_rate.setToolTip(learning_rate_tip)

        loss_function_tip = "Loss function to be used."
        self.loss_function_label.setToolTip(loss_function_tip)
        self.loss_function.setToolTip(loss_function_tip)

        dropout_rate_tip = "Fraction of the input units to drop."
        self.dropout_rate_label.setToolTip(dropout_rate_tip)
        self.dropout_rate.setToolTip(dropout_rate_tip)

        early_stopping_tip = "Whether to use early stopping in training."
        self.early_stopping_label.setToolTip(early_stopping_tip)
        self.early_stopping.setToolTip(early_stopping_tip)

        es_patience_tip = "Number of epochs with no improvement after which training will be stopped."
        self.es_patience_label.setToolTip(es_patience_tip)
        self.es_patience.setToolTip(es_patience_tip)
