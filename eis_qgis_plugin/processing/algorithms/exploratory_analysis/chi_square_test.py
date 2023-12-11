from qgis.core import (
    QgsProcessingParameterField,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
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
        self.alg_parameters = ["input_file", "target_column", "columns", "output_file"]

        self.addParameter(
            QgsProcessingParameterFile(
                name=self.alg_parameters[0], description="Input file"
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.alg_parameters[1],
                description="Target column",
                parentLayerParameterName=self.alg_parameters[0],
                defaultValue=None
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.alg_parameters[2],
                description="Columns to test against target column",
                allowMultiple=True,
                parentLayerParameterName=self.alg_parameters[0],
                defaultValue=None
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[3], description="Output file"
            )
        )
