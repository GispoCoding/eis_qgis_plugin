from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFile,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPredictWithTrainedModel(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "predict_with_trained_model"
        self._display_name = "Predict with trained model"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = "Predict mineral prospectivity with a trained machine learning model."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "model_file",
            "output_raster"
        ]

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                name=self.alg_parameters[0], description="Input data", layerType=QgsProcessing.TypeRaster
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                name=self.alg_parameters[1], description="Model file", fileFilter='.joblib (*.joblib)'
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[2],
                description="Output raster",
            )
        )
