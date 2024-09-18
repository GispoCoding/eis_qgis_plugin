from typing import Any, Dict, Optional

from qgis.core import (
    QgsProcessing,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterMapLayer,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm
from eis_qgis_plugin.utils.misc_utils import parse_string_list_parameter_and_run_command


class EISMlpClassifier(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "mlp_classifier_train"
        self._display_name = "MLP classifier"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = """
        Train MLP (Multilayer Perceptron) classifier using Keras.

        Creates a Sequential model with Dense NN layers. For each element in `neurons`, Dense layer with \
        corresponding dimensionality/neurons is created with the specified activation function (`activation`). \
        If `dropout_rate` is specified, a Dropout layer is added after each Dense layer.

        Parameters default to a binary classification model using sigmoid as last activation, binary \
        crossentropy as loss function and 1 output neuron/unit.

        For more information about Keras models, read the documentation here: https://keras.io/.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "target_labels",
            "validation_split",
            # "validation_data",
            "neurons",
            "output_neurons",
            "activation",
            "last_activation",
            "epochs",
            "batch_size",
            "optimizer",
            "learning_rate",
            "loss_function",
            "dropout_rate",
            "early_stopping",
            "es_patience",
            "validation_metrics",
            "random_state",
            "output_file"
        ]

        evidence_data_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[0], description="Evidence data", layerType=QgsProcessing.TypeRaster
        )
        evidence_data_param.setHelp("Evidence rasters used for training.")
        self.addParameter(evidence_data_param)

        target_labels_param = QgsProcessingParameterMapLayer(
            name=self.alg_parameters[1], description="Target labels"
        )
        target_labels_param.setHelp("Target labels used for training.")
        self.addParameter(target_labels_param)

        validation_split_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Validation split",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=0.2,
            minValue=0.001,
            maxValue=0.999
        )
        validation_split_param.setHelp("Fraction of data used for validation during training.")
        self.addParameter(validation_split_param)

        # NOTE: Not implemented yet
        # validation_data_param = QgsProcessingParameterNumber(
        #     name=self.alg_parameters[3], description="Validation data"
        # )
        # validation_data_param.setHelp("")
        # self.addParameter(validation_data_param)

        neurons_param = QgsProcessingParameterString(
            name=self.alg_parameters[3], description="Neurons",
        )
        neurons_param.setHelp(
            "Number of neurons in each hidden layer. Input the neurons as a comma-separated list. \
            For example: 10, 5, 10."
        )
        self.addParameter(neurons_param)

        output_neurons_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4], description="Output neurons", minValue=1, defaultValue=1
        )
        output_neurons_param.setHelp("Number of neurons in the output layer.")
        self.addParameter(output_neurons_param)

        activation_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[5],
            description="Activation",
            options=["relu", "linear", "sigmoid", "tanh"],
            defaultValue=0
        )
        activation_param.setHelp("Activation function used in each hidden layer.")
        self.addParameter(activation_param)

        last_activation_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[6], description="Last activation", options=["sigmoid", "softmax"], defaultValue=0
        )
        last_activation_param.setHelp("Activation function used in the output layer.")
        self.addParameter(last_activation_param)

        epochs_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[7],
            description="Epochs",
            minValue=1,
            defaultValue=50
        )
        epochs_param.setHelp("Number of epochs to train the model.")
        self.addParameter(epochs_param)

        batch_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[8],
            description="Batch size",
            minValue=1,
            defaultValue=32
        )
        batch_size_param.setHelp("Number of samples per gradient update.")
        self.addParameter(batch_size_param)

        optimizer_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[9],
            description="Optimizer",
            options=["adam", "adagrad", "rmsprop", "sdg"],
            defaultValue=0
        )
        optimizer_param.setHelp("Optimizer to be used.")
        self.addParameter(optimizer_param)

        learning_rate_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[10],
            description="Learning rate",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=0.001,
            minValue=0.0001
        )
        learning_rate_param.setHelp("Learning rate to be used in training.")
        self.addParameter(learning_rate_param)

        loss_function_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[11],
            description="Loss function",
            options=["binary_crossentropy", "categorical_crossentropy"],
            defaultValue=0
        )
        loss_function_param.setHelp("Loss function to be used.")
        self.addParameter(loss_function_param)

        dropout_rate_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[12],
            description="Dropout rate",
            type=QgsProcessingParameterNumber.Double,
            optional=True,
            minValue=0,
            maxValue=1
        )
        dropout_rate_param.setHelp("Fraction of the input units to drop.")
        self.addParameter(dropout_rate_param)

        early_stopping_param = QgsProcessingParameterBoolean(
            name=self.alg_parameters[13],
            description="Early stopping",
            defaultValue=True
        )
        early_stopping_param.setHelp("Whether to use early stopping in training.")
        self.addParameter(early_stopping_param)

        es_patience_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[14],
            description="Early stopping patience",
            minValue=1,
            defaultValue=5,
        )
        es_patience_param.setHelp("Number of epochs with no improvement after which training will be stopped.")
        self.addParameter(es_patience_param)

        validation_metrics_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[15],
            description="Metrics",
            options=["accuracy", "precision", "recall"],
            allowMultiple=True,
            defaultValue=0
        )
        validation_metrics_param.setHelp("Metrics to use for scoring the model during training.")
        self.addParameter(validation_metrics_param)

        random_state_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[16],
            description="Random state",
            optional=True,
            minValue=0
        )
        random_state_param.setHelp(
            "Seed for random number generation. Sets Python, Numpy and Tensorflow seeds to make program deterministic."
        )
        self.addParameter(random_state_param)

        output_model_param = QgsProcessingParameterFileDestination(
            name=self.alg_parameters[17],
            description="Output model",
            fileFilter='.joblib (*.joblib)'
        )
        output_model_param.setHelp("The trained model saved to file.")
        self.addParameter(output_model_param)


    def processAlgorithm(
        self,
        parameters: Dict[str, QgsProcessingParameterDefinition],
        context: QgsProcessingContext,
        feedback: Optional[QgsProcessingFeedback]
    ) -> Dict[str, Any]:
        if feedback is None:
            feedback = QgsProcessingFeedback()

        results = parse_string_list_parameter_and_run_command(
            self,
            3,
            parameters,
            context,
            feedback
        )

        return results
