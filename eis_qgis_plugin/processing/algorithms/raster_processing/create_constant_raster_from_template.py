from qgis.core import (
    QgsProcessingParameterCrs,
    QgsProcessingParameterExtent,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISCreateConstantRasterFromTemplate(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "create_constant_raster_from_template"
        self._display_name = "Create constant raster from template"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Create a constant raster based on a template raster."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "constant_value",
            "template_raster",
            "extent",
            "target_epsg",
            "target_pixel_size",
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

        template_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[1],
            description="Template raster",
            optional=True,
        )
        template_raster_param.setHelp("An optional raster to use as a template for the output.")
        self.addParameter(template_raster_param)

        extent_param = QgsProcessingParameterExtent(
            name=self.alg_parameters[2], description="Raster extent", optional=True
        )
        extent_param.setHelp("The extent of the output raster.")
        self.addParameter(extent_param)

        target_epsg_param = QgsProcessingParameterCrs(
            name=self.alg_parameters[3],
            description="Coordinate system",
        )
        target_epsg_param.setHelp("The EPSG code for the output raster.")
        self.addParameter(target_epsg_param)

        target_pixel_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4],
            description="Target pixel size",
            optional=True,
        )
        target_pixel_size_param.setHelp("The pixel size of the output raster.")
        self.addParameter(target_pixel_size_param)

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
