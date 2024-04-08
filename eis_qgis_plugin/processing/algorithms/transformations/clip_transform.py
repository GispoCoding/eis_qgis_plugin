from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISClipTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "clip_transform"
        self._display_name = "Clip transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = """
            Clips data based on specified upper and lower limits.

            Replaces values below the lower limit and above the upper limit with provided values, respecively.
            Works both one-sided and two-sided but raises error if no limits provided.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "limit_lower",
            "limit_higher",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("Input raster to be clipped.")
        self.addParameter(input_raster_param)

        lower_limit_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Lower",
            type=QgsProcessingParameterNumber.Double,
            optional=True,
        )
        lower_limit_param.setHelp("Lower transformation limit.")
        self.addParameter(lower_limit_param)

        higher_limit_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Higher",
            type=QgsProcessingParameterNumber.Double,
            optional=True,
        )
        higher_limit_param.setHelp("Higher transformation limit.")
        self.addParameter(higher_limit_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Output raster"
        )
        output_raster_param.setHelp("Output raster with transformed data.")
        self.addParameter(output_raster_param)
