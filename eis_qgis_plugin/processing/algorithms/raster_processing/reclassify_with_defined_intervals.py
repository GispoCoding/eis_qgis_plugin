from qgis.core import (
    QgsProcessingParameterBand,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISReclassifyWithDefinedIntervals(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "reclassify_with_defined_intervals"
        self._display_name = "Reclassify with defined intervals"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = (
            "Reclassify raster data set with defined intervals."
        )

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "interval_size",
            "bands",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("The input raster data set.")
        self.addParameter(input_raster_param)

        interval_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Interval size",
            minValue=1,
        )
        interval_size_param.setHelp("The interval size for Defined intervals.")
        self.addParameter(interval_size_param)

        bands_param = QgsProcessingParameterBand(
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
