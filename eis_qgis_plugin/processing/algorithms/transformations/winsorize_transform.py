from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISWinsorizeTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "winsorize_transform"
        self._display_name = "Winsorize transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = """
            Winsorize data based on specified percentile values.

            Replaces values between [minimum, lower percentile] and [upper percentile, maximum] if provided. \
            Works both one-sided and two-sided but raises error if no percentile values provided.

            Percentiles are symmetrical, i.e. percentile_lower = 10 corresponds to the interval [min, 10%]. \
            And percentile_upper = 10 corresponds to the intervall [90%, max]. \
            I.e. percentile_lower = 0 refers to the minimum and percentile_upper = 0 to the data maximum.

            Calculation of percentiles is ambiguous. Users can choose whether to use the value \
            for replacement from inside or outside of the respective interval. Example: \
            Given the np.array[5 10 12 15 20 24 27 30 35] and percentiles(10, 10), the calculated \
            percentiles are (5, 35) for inside and (10, 30) for outside. \
            This results in [5 10 12 15 20 24 27 30 35] and [10 10 12 15 20 24 27 30 30], respectively.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "percentile_lower",
            "percentile_higher",
            "inside",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("Input raster to be transformed.")
        self.addParameter(input_raster_param)

        lower_perecentile_param = QgsProcessingParameterNumber(
                name=self.alg_parameters[1],
                description="Lower percentile",
                type=QgsProcessingParameterNumber.Double,
                minValue=0.0,
                maxValue=100.0,
                optional=True,
            )
        lower_perecentile_param.setHelp("Lower percentile value.")
        self.addParameter(lower_perecentile_param)

        higher_percentile_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Higher percentile",
            type=QgsProcessingParameterNumber.Double,
            minValue=0.0,
            maxValue=100.0,
            optional=True,
        )
        higher_percentile_param.setHelp("Higher percentile value.")
        self.addParameter(higher_percentile_param)

        inside_param = QgsProcessingParameterBoolean(
            name=self.alg_parameters[3], description="Inside", defaultValue=False
        )
        inside_param.setHelp(
            "Whether to use the value for replacement from the left or right of the calculated percentile."
        )
        self.addParameter(inside_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[4], description="Output raster"
        )
        output_raster_param.setHelp("Output raster with the transformed data.")
        self.addParameter(output_raster_param)
