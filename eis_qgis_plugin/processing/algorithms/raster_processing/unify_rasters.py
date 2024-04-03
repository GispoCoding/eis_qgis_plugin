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
        self._short_help_string = """
            Unify (reproject, resample, align/snap and optionally clip) given rasters with a base raster.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "rasters_to_unify",
            "base_raster",
            "resampling_method",
            "same_extent",
            "output_directory"
        ]

        rasters_to_unify_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[0], description="Rasters to unify", layerType=QgsProcessing.TypeRaster
        )
        rasters_to_unify_param.setHelp("Rasters to be unified with the base raster.")
        self.addParameter(rasters_to_unify_param)

        base_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[1], description="Base raster"
        )
        base_raster_param.setHelp("The base raster to define target raster grid properties.")
        self.addParameter(base_raster_param)

        resampling_method_param = QgsProcessingParameterEnum(
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
            defaultValue=0,
        )
        resampling_method_param.setHelp(
            "The resampling method used if resampling is needed."
        )
        self.addParameter(resampling_method_param)

        same_extent_param = QgsProcessingParameterBoolean(
            name=self.alg_parameters[3], description="Same extent"
        )
        same_extent_param.setHelp(
            "If the unified rasters will be forced to have the same extent/bounds \
            as the base raster. Expands smaller rasters with nodata cells."
        )
        self.addParameter(same_extent_param)

        output_directory_param = QgsProcessingParameterFolderDestination(
            name=self.alg_parameters[4], description="Output directory"
        )
        output_directory_param.setHelp("Output directory to save the unified raster to.")
        self.addParameter(output_directory_param)
