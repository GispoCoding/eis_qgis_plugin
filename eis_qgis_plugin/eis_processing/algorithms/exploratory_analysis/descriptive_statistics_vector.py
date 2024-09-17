from qgis.core import QgsProcessingParameterFeatureSource, QgsProcessingParameterField

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISDescriptiveStatisticsVector(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "descriptive_statistics_vector"
        self._display_name = "Descriptive statistics (vector)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
            Calculate descriptive statistics for vector data.

            Calculates min, max, mean, quantiles (25%, 50% and 75%), \
            standard deviation, relative standard deviation and skewness.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_file", "column"]

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector to calculate descriptive statistics for.")
        self.addParameter(input_vector_param)

        column_param = QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Column",
            parentLayerParameterName=self.alg_parameters[0],
        )
        column_param.setHelp("Column selection.")
        self.addParameter(column_param)
