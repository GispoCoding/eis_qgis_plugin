from qgis.core import (
    QgsProcessingParameterCrs,
    QgsProcessingParameterExtent,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISCreateConstantRasterManually(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "create_constant_raster_manually"
        self._display_name = "Create constant raster manually"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Create a constant raster manually."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "constant_value",
            "target_epsg",
            "target_pixel_size",
            "raster_width",
            "raster_height",
            "nodata_value",
            "output_raster",
        ]

        constant_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[0],
            description="Constant value",
            type=QgsProcessingParameterNumber.Double,
        )
        constant_value_param.setHelp("The constant value to use in the raster.")
        self.addParameter(constant_value_param)

        target_epsg_param = QgsProcessingParameterCrs(
            name=self.alg_parameters[1],
            description="Coordinate system",
        )
        target_epsg_param.setHelp("The EPSG code for the output raster.")
        self.addParameter(target_epsg_param)

        target_pixel_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Target pixel size",
        )
        target_pixel_size_param.setHelp("The pixel size of the output raster.")
        self.addParameter(target_pixel_size_param)

        raster_width_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            description="Raster width",
        )
        raster_width_param.setHelp("The width of the output raster.")
        self.addParameter(raster_width_param)

        raster_height_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4],
            description="Raster height",
        )
        raster_height_param.setHelp("The height of the output raster.")
        self.addParameter(raster_height_param)

        nodata_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[5],
            description="Nodata value",
            optional=True,
            type=QgsProcessingParameterNumber.Double,
        )
        nodata_value_param.setHelp("The nodata value of the output raster.")
        self.addParameter(nodata_value_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[6], description="Output raster"
        )
        output_raster_param.setHelp("The Output raster.")
        self.addParameter(output_raster_param)
