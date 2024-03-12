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
            "validation_metric",
            "output_raster"
        ]

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                name=self.alg_parameters[0], description="Input data", layerType=QgsProcessing.TypeRaster
            )
        )

        self.addParameter(
            QgsProcessingParameterMapLayer(
                name=self.alg_parameters[1], description="Target labels"
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                name=self.alg_parameters[2], description="Model file", fileFilter='.joblib (*.joblib)'
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[3],
                description="Evaluation metric",
                options=["accuracy", "precision", "recall", "f1", "auc", "mse", "rmse", "mae", "r2"],
                defaultValue="accuracy",
                allowMultiple=True
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[4],
                description="Output raster",
            )
        )
