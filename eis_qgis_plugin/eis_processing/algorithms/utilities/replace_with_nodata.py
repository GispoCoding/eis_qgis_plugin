from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISReplaceWithNodata(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "replace_with_nodata"
        self._display_name = "Replace with nodata"
        self._group = "Utilities"
        self._group_id = "utilities"
        self._short_help_string = """
        Replace raster pixel values with nodata.
        
        Can be used either for replacing all pixels with certain value with nodata, or for replacing all pixels with \
        values less than, greater than, less than or equal to, or greater than or equal to the target value with nodata.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "target_value", "nodata_value", "replace_condition", "output_raster"]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("Input raster with pixels to be replaced with nodata.")
        self.addParameter(input_raster_param)

        target_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1], description="Target value"
        )
        target_value_param.setHelp("Target pixel value to be replaced with nodata.")
        self.addParameter(target_value_param)

        nodata_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2], description="Nodata value", optional=True
        )
        nodata_value_param.setHelp("Value used as nodata.")
        self.addParameter(nodata_value_param)

        replace_condition_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[3],
            description="Replace condition",
            options=[
                "equal",
                "less_than",
                "greater_than",
                "less_than_or_equal",
                "greater_than_or_equal"
            ],
            defaultValue="equal"
        )
        replace_condition_param.setHelp(
            "Whether to replace single values ('equal'), or multiple values based on condition.'"
        )
        self.addParameter(replace_condition_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[4], description="Replace with nodata output"
        )
        output_raster_param.setHelp(
            "Output raster with specified pixel values replaced with nodata."
        )
        self.addParameter(output_raster_param)
