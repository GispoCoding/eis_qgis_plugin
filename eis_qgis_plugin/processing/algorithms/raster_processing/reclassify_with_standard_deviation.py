from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterString,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISReclassifyWithStandardDeviation(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "reclassify_with_standard_deviation"
        self._display_name = "Reclassify with standard deviation"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = (
            "Reclassify raster data set with standard deviation."
        )

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "number_of_intervals",
            "bands",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("The input raster data set.")
        self.addParameter(input_raster_param)

        interval_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1], description="Number of standard deviations"
        )
        interval_size_param.setHelp("The number of standard deviation.")
        self.addParameter(interval_size_param)

        bands_param = QgsProcessingParameterString(
            name=self.alg_parameters[2],
            description="Bands",
            optional=True,
        )
        bands_param.setHelp("The bands to be reclassified.")
        self.addParameter(bands_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Output raster"
        )
        output_raster_param.setHelp("The output raster data set.")
        self.addParameter(output_raster_param)
