from qgis.core import (
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISUnifyRasters(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "unify_rasters"
        self._display_name = "Unify rasters"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Unify a set of rasters"

    def initAlgorithm(self, config=None):

        self.alg_parameters = ["base_raster", "rasters", "output_raster"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Base raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[1], description="Raster(s) to unify"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[2], description="Output raster"
            )
        )
