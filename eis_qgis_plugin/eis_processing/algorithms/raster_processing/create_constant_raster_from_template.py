from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISCreateConstantRasterFromTemplate(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "create_constant_raster_from_template"
        self._display_name = "Create constant raster from template"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Create a constant raster from a template raster."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "constant_value",
            "template_raster",
            "nodata_value",
            "output_raster",
        ]

        constant_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[0],
            description="Constant value",
            type=QgsProcessingParameterNumber.Double,
        )
        constant_value_param.setHelp("The constant value of the output raster.")
        self.addParameter(constant_value_param)

        template_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[1],
            description="Template/base raster",
        )
        template_raster_param.setHelp("The raster to use as the template for the output raster grid properties.")
        self.addParameter(template_raster_param)

        nodata_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Nodata value",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=-9999
        )
        nodata_value_param.setHelp("The nodata value of the output raster.")
        self.addParameter(nodata_value_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Output raster"
        )
        output_raster_param.setHelp("The output constant raster.")
        self.addParameter(output_raster_param)
