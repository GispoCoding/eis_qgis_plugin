from qgis.core import QgsProcessingParameterBand, QgsProcessingParameterRasterLayer

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISDescriptiveStatisticsRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "descriptive_statistics_raster"
        self._display_name = "Descriptive statistics (raster)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
            Compute descriptive statistics for raster data.

            Computes the following statistics:
            - min
            - max
            - mean
            - quantile 25%
            - quantile 50% (median)
            - quantile 75%
            - standard deviation
            - relative standard deviation
            - skewness

            Nodata values are removed from the data before the statistics are computed.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "band"]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("Input raster.")
        self.addParameter(input_raster_param)

        band_param =QgsProcessingParameterBand(
            name=self.alg_parameters[1], description="Band", parentLayerParameterName=self.alg_parameters[0]
        )
        band_param.setHelp("Raster band to compute descriptive statistics from.")
        self.addParameter(band_param)
