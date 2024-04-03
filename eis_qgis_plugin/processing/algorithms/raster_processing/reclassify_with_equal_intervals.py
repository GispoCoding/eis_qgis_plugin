from qgis.core import (
    QgsProcessingParameterBand,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISReclassifyWithEqualIntervals(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "reclassify_with_equal_intervals"
        self._display_name = "Reclassify with equal intervals"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Reclassify raster with equal intervals."

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
        input_raster_param.setHelp("The input raster to be reclassified.")
        self.addParameter(input_raster_param)

        interval_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Number of intervals",
            minValue=2,
        )
        interval_size_param.setHelp("The number of intervals used in reclassification.")
        self.addParameter(interval_size_param)

        bands_param = QgsProcessingParameterBand(
            name=self.alg_parameters[2],
            description="Raster band",
            parentLayerParameterName=self.alg_parameters[0],
        )
        bands_param.setHelp("The band to be reclassified.")
        self.addParameter(bands_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Output raster"
        )
        output_raster_param.setHelp("The output reclassfied raster.")
        self.addParameter(output_raster_param)
