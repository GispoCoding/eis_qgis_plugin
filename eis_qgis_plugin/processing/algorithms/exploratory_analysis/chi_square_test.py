from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterString,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISChiSquareTest(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "chi_square_test"
        self._display_name = "Chi-square test"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Compute Chi-square test for independence on the input data."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_geometries", "target_column", "columns", "output_file"]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input geometries"
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                name=self.alg_parameters[1],
                description="Target column",
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                name=self.alg_parameters[2],
                description="Columns to test against target column",
                multiLine=True,
                defaultValue=None
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[3], description="Output file"
            )
        )
