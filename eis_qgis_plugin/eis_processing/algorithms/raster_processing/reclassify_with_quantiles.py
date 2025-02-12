from qgis.core import (
    QgsProcessingParameterBand,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISReclassifyWithQuantiles(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "reclassify_with_quantiles"
        self._display_name = "Reclassify with quantiles"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = """
        Reclassify raster with quantiles.
        
        If bands are not given, all bands are used for classification.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "number_of_quantiles",
            "bands",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("The input raster to be reclassified.")
        self.addParameter(input_raster_param)

        quantiles_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Quantiles",
            minValue=2,
        )
        quantiles_param.setHelp("The number of quantiles used in reclassification.")
        self.addParameter(quantiles_param)

        bands_param = QgsProcessingParameterBand(
            name=self.alg_parameters[2],
            description="Raster band",
            parentLayerParameterName=self.alg_parameters[0],
        )
        bands_param.setHelp("The band to be reclassified.")
        self.addParameter(bands_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Reclassified raster (quantiles)"
        )
        output_raster_param.setHelp("The output reclassified raster.")
        self.addParameter(output_raster_param)
