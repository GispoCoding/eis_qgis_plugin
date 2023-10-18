from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISClipRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "clip_raster"
        self._display_name = "Clip raster"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Clip a raster with vector layer features."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "geometries", "output_raster"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[1],
                description="Areas to be clipped",
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[2], description="Output raster"
            )
        )
