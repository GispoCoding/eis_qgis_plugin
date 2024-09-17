from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISUnifyRasters(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "unify_rasters"
        self._display_name = "Unify rasters"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = """
            Unifies given rasters with the base raster.

            Performs the following operations:
            - Reprojecting
            - Resampling
            - Aligning / snapping
            - Clipping / expanding extents (optional, determined by masking parameter)
            - Copying nodata cells from base raster (optional, determined by masking parameter)
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "rasters_to_unify",
            "base_raster",
            "resampling_method",
            "masking",
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

        masking = QgsProcessingParameterEnum(
            name=self.alg_parameters[3],
            description="Masking",
            options=[
                "None",
                "Extents",
                "Full",
            ],
            defaultValue=1,
        )
        masking.setHelp(
            "Controls if and how masking should be handled. If `extents`, the bounds of rasters to-be-unified \
            are matched with the base raster. Larger rasters are clipped and smaller rasters expanded (with nodata). \
            If `extents_and_nodata`, copies nodata pixel locations from the base raster additionally. If None, \
            extents are not matched and nodata not copied."
        )
        self.addParameter(masking)

        output_directory_param = QgsProcessingParameterFolderDestination(
            name=self.alg_parameters[4], description="Output directory"
        )
        output_directory_param.setHelp("Output directory to save the unified raster to.")
        self.addParameter(output_directory_param)
