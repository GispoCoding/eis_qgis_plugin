from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFileDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISNormalityTest(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "normality_test"
        self._display_name = "Normality test"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Compute Shapiro-Wilk test for normality on the input data."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_file", "output_file"]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input geometries"
            )
        )


        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[1], description="Output file"
            )
        )
