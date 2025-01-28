from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISMinMaxScaling(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "min_max_scaling"
        self._display_name = "Min-max scale"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = """
            Normalize data based on a specified new range.

            Uses the provided new minimum and maximum to transform data into the new interval. \
            Performs normalization with default min and max values.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "min", "max", "output_raster"]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("")
        self.addParameter(input_raster_param)

        min_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Min",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=0.0,
        )
        min_param.setHelp("Min value of the new interval data will be transformed into.")
        self.addParameter(min_param)

        max_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Max",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=1.0,
        )
        max_param.setHelp("Max value of the new interval data will be transformed into.")
        self.addParameter(max_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Min-max scaled raster"
        )
        output_raster_param.setHelp("Output raster with transformed data.")
        self.addParameter(output_raster_param)
