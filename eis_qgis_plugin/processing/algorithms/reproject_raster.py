from qgis.core import (
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterCrs,
    QgsProcessingParameterEnum,
    QgsProcessingParameterRasterDestination
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm

class EISReprojectRaster(EISProcessingAlgorithm):

    def __init__(self) -> None:
        super().__init__()

        self._name = "reproject_raster"
        self._display_name = "Reproject raster"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Reproject raster to a target coordinate reference system"

    def initAlgorithm(self, config=None):

        self.alg_parameters = ["input_raster", "crs", "resampling_method", "output_raster"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name = self.alg_parameters[0],
                description = "Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterCrs(
                name = self.alg_parameters[1],
                description = "Target CRS",
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name = self.alg_parameters[2],
                description = "Resampling method",
                options = ["Nearest" , "Bilinear" , "Cubic" , "Average" , "Gauss" , "Max" , "Min"],
                defaultValue = "Nearest",
                usesStaticStrings=True
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name = self.alg_parameters[3],
                description = "Output raster"
            )
        )
