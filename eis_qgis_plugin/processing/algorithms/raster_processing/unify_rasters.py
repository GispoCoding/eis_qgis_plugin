from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterMultipleLayers,
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
        self.alg_parameters = [
            "base_raster",
            "rasters_to_unify",
            "resampling_method",
            "same_extent",
            "output_directory"
        ]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Base raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                name=self.alg_parameters[1], description="Rasters to unify", layerType=QgsProcessing.TypeRaster
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[2],
                description="Resampling method",
                options=[
                    "Nearest",
                    "Bilinear",
                    "Cubic",
                    "Average",
                    "Gauss",
                    "Max",
                    "Min",
                ],
                defaultValue="Nearest",
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                name=self.alg_parameters[3], description="Same extent"
            )
        )

        self.addParameter(
            QgsProcessingParameterFolderDestination(
                name=self.alg_parameters[4], description="Output directory"
            )
        )
