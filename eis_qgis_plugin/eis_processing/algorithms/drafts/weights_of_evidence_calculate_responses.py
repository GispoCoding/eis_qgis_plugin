from qgis.core import (
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISWeightsOfEvidenceCalculateResponses(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "weights_of_evidence_calculate_responses"
        self._display_name = "Weights of evidence calculate responses"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = (
            "Calculate responses for weights of evidence calculations"
        )

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "deposits",
            "output_rasters",
        ]

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                name=self.alg_parameters[0],
                description="Weight rasters",
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                name=self.alg_parameters[1], description="Mineral deposits"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[2], description="Output raster"
            )
        )
