from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFile,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISRegressorPredict(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "regressor_predict"
        self._display_name = "Regressor predict"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = "Predict mineral prospectivity with a trained machine learning regressor model."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "model_file",
            "output_raster"
        ]

        evidence_data_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[0], description="Evidence data", layerType=QgsProcessing.TypeRaster
        )
        evidence_data_param.setHelp(
            "Evidence data used for predicting. Evidence layers should match the layers used in training."
        )
        self.addParameter(evidence_data_param)

        model_file_param = QgsProcessingParameterFile(
            name=self.alg_parameters[1], description="Model file", fileFilter='.joblib (*.joblib)'
        )
        model_file_param.setHelp("The model file.")
        self.addParameter(model_file_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[2],
            description="Output raster",
        )
        output_raster_param.setHelp("Output raster with predictions.")
        self.addParameter(output_raster_param)
