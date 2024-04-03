from qgis.core import QgsProcessingParameterRasterLayer

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISDescriptiveStatisticsRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "descriptive_statistics_raster"
        self._display_name = "Descriptive statistics (raster)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
            Calculate descriptive statistics for raster data.

            Calculates min, max, mean, quantiles (25%, 50% and 75%), \
            standard deviation, relative standard deviation and skewness.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_file"]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("Input raster to calculate descriptive statistics for.")
        self.addParameter(input_raster_param)
