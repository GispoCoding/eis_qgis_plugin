from qgis.core import (
    QgsProcessingParameterBand,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)
from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISReclassifyWithNaturalBreaks(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "reclassify_with_natural_breaks"
        self._display_name = "Reclassify with natural breaks"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = (
            "Reclassify raster data set with natural breaks."
        )

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "number_of_classes",
            "bands",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("The input raster data set.")
        self.addParameter(input_raster_param)

        breaks_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="The number of classes",
            minValue=2,
        )
        breaks_param.setHelp("The number of classes for Natural breaks.")
        self.addParameter(breaks_param)

        bands_param = QgsProcessingParameterBand(
            name=self.alg_parameters[2],
            description="Raster bands",
            optional=True,
        )
        bands_param.setHelp("The bands to be reclassified.")
        self.addParameter(bands_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Output raster"
        )
        output_raster_param.setHelp("The output raster data set.")
        self.addParameter(output_raster_param)
