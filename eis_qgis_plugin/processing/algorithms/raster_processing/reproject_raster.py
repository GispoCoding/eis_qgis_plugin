from qgis.core import (
    QgsProcessingParameterCrs,
    QgsProcessingParameterEnum,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISReprojectRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "reproject_raster"
        self._display_name = "Reproject raster"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Reproject raster to a target coordinate reference system."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "target_crs",
            "resampling_method",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("Input raster to be reprojected.")
        self.addParameter(input_raster_param)

        target_crs_param = QgsProcessingParameterCrs(
            name=self.alg_parameters[1],
            description="Target CRS",
        )
        target_crs_param.setHelp("Target coordinate reference system.")
        self.addParameter(target_crs_param)

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
            "The resampling method. Most suitable method depends on the dataset and context."
        )
        self.addParameter(resampling_method_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Output raster"
        )
        output_raster_param.setHelp("The output reprojected raster.")
        self.addParameter(output_raster_param)
