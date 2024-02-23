from qgis.core import (
    QgsProcessingParameterBand,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterString,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISReclassifyWithManualBreaks(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "reclassify_with_manual_breaks"
        self._display_name = "Reclassify with manual breaks"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = (
            "Reclassify raster data set with manual breaks."
        )

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "breaks",
            "bands",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("The input raster data set.")
        self.addParameter(input_raster_param)

        breaks_param = QgsProcessingParameterString(
            name=self.alg_parameters[1],
            description="Breaks"
        )
        breaks_param.setHelp(
            '''The breaks for Manual breaks. Input the breaks as a comma-separated list. 
            For example: 0, 10, 20, 30, 40, 50.'''
        )
        self.addParameter(breaks_param)

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
