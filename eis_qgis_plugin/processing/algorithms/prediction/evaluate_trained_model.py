from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFile,
    QgsProcessingParameterMapLayer,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISEvaluateTrainedModel(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "evaluate_trained_model"
        self._display_name = "Evaluate trained model"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = "Evaluate/score a trained machine learning model using test data."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "target_labels",
            "model_file",
            "validation_metrics",
            "output_raster"
        ]

        evidence_data_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[0], description="Evidence data", layerType=QgsProcessing.TypeRaster
        )
        evidence_data_param.setHelp(
            "Evidence data used for testing. Evidence layers should match the layers used in training."
        )
        self.addParameter(evidence_data_param)

        target_labels_param = QgsProcessingParameterMapLayer(
            name=self.alg_parameters[1], description="Target labels"
        )
        target_labels_param.setHelp("Target labels used for evaluating performance.")
        self.addParameter(target_labels_param)

        model_file_param = QgsProcessingParameterFile(
            name=self.alg_parameters[2], description="Model file", fileFilter='.joblib (*.joblib)'
        )
        model_file_param.setHelp("The model file.")
        self.addParameter(model_file_param)

        evaluation_metric_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[3],
            description="Evaluation metric",
            options=["accuracy", "precision", "recall", "f1", "auc", "mse", "rmse", "mae", "r2"],
            defaultValue="accuracy",
            allowMultiple=True
        )
        evaluation_metric_param.setHelp(
            "Metrics calculated. The selected metrics need to be applicable for model type (classifier or regressor)."
        )
        self.addParameter(evaluation_metric_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[4],
            description="Output raster",
        )
        output_raster_param.setHelp("Output raster with predictions.")
        self.addParameter(output_raster_param)
