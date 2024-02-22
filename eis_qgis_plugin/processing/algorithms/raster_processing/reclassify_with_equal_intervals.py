from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISReclassifyWithDefinedIntervals(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "reclassify_with_equal_intervals"
        self._display_name = "Reclassify with equal intervals"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = (
            "Reclassify raster data set with equal intervals."
        )

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "number_of_intervals",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("The input raster data set.")
        self.addParameter(input_raster_param)

        interval_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1], description="Number of intervals"
        )
        interval_size_param.setHelp("The number of intervals for Equal intervals.")
        self.addParameter(interval_size_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[2], description="Output raster"
        )
        output_raster_param.setHelp("The output raster data set.")
        self.addParameter(output_raster_param)
