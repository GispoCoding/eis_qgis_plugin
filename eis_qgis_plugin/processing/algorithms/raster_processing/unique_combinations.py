from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISUniqueCombinations(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "unique_combinations"
        self._display_name = "Unique combinations"
        self._group = "Unique Combinations"
        self._group_id = "raster_processing"
        self._short_help_string = "Get combinations of raster values between rasters"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "output_raster"
        ]

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                name=self.alg_parameters[0],
                description="Input raster or rasters",
                layerType=QgsProcessing.TypeRaster,
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[1],
                description="Output raster"
            )
        )
