from qgis.core import (
    QgsProcessingParameterBand,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISCalculateBaseMetrics(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "calculate_base_metrics"
        self._display_name = "Calculate base metrics"
        self._group = "Evaluation"
        self._group_id = "evaluation"
        self._display_name = "Calculate base metrics"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "input_deposits",
            "band",
            "negatives",
            "output_metrics",
        ]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                name=self.alg_parameters[1], description="Mineral deposits"
            )
        )

        self.addParameter(
            QgsProcessingParameterBand(
                name=self.alg_parameters[2], description="Raster band", defaultValue=1
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                name=self.alg_parameters[3],
                description="Negative locations",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[4], description="Output metrics"
            )
        )
