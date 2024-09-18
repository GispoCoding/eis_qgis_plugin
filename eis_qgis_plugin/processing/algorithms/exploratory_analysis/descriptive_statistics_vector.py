from qgis.core import QgsProcessingParameterFeatureSource, QgsProcessingParameterField

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISDescriptiveStatisticsVector(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "descriptive_statistics_vector"
        self._display_name = "Descriptive statistics (vector)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
            Compute descriptive statistics for vector data.

            Computes the following statistics:
            - min
            - max
            - mean
            - quantiles 25%
            - quantile 50% (median)
            - quantile 75%
            - standard deviation
            - relative standard deviation
            - skewness
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_file", "column"]

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector.")
        self.addParameter(input_vector_param)

        column_param = QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Column",
            parentLayerParameterName=self.alg_parameters[0],
            type=QgsProcessingParameterField.Numeric,
        )
        column_param.setHelp("Column in vector data to compute descriptive statistics from.")
        self.addParameter(column_param)
