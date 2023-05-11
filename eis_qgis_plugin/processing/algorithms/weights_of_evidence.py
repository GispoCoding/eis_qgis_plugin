from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISWeightsOfEvidence(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "weights_of_evidence"
        self._display_name = "Weights of evidence"
        self._group = "Modelling"
        self._group_id = "modelling"
        self._short_help_string = "Compute weights of evidence"

    def initAlgorithm(self, config=None):

        self.alg_parameters = [
            "evidential_raster",
            "deposit_raster",
            "weights_type",
            "contrast",
            "output_raster",
        ]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Geospatial evidential raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[1], description="Mineral deposits raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[2],
                description="Weights of evidence computations type",
                options=[
                    "Unique weights",
                    "Cumulative ascending weights",
                    "Cumulative descending weights",
                ],
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[3],
                description="Studentized contrast value",
                type=QgsProcessingParameterNumber.Double,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[4], description="Output raster"
            )
        )
