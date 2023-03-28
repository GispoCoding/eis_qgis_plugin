from qgis.core import (
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterRasterDestination
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm

class EISSnapRaster(EISProcessingAlgorithm):

    def __init__(self) -> None:
        super().__init__()

        self._name = "snap_raster"
        self._display_name = "Snap raster"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Snap a raster to same alignment with base raster"

    def initAlgorithm(self, config=None):

        self.alg_parameters = ["input_raster", "base_raster", "output_raster"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name = self.alg_parameters[0],
                description = "Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name = self.alg_parameters[1],
                description = "Base raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name = self.alg_parameters[2],
                description = "Output raster"
            )
        )
