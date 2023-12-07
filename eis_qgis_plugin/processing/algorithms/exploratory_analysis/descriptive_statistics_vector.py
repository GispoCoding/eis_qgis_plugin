from qgis.core import QgsProcessingParameterFeatureSource, QgsProcessingParameterField

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISDescriptiveStatisticsVector(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "descriptive_statistics_vector"
        self._display_name = "Descriptive statistics (vector)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Generate descriptive statistics for a vector layer"

    def initAlgorithm(self, config=None):
        # self.alg_parameters = ["input_file", "column", "output_file"]
        self.alg_parameters = ["input_file", "column"]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input layer"
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.alg_parameters[1],
                description="Column",
                parentLayerParameterName=self.alg_parameters[0],
            )
        )

        # self.addParameter(
        #     QgsProcessingParameterFileDestination(
        #         name=self.alg_parameters[2],
        #         description="Output file",
        #     )
        # )
