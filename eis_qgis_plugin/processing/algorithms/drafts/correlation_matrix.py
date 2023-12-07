from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterNumber,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISCorrelationMatrix(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "correlation_matrix"
        self._display_name = "Correlation matrix"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Compute correlation matrix on the input data."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_data", "correlation_method", "min_periods", "output_file"]

        self.addParameter(
            QgsProcessingParameterFile(
                name=self.alg_parameters[0], description="Input data (numeric)"
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[1],
                description="Target column",
                options=["pearson", "kendall", "spearman"],
                defaultValue="pearson"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2],
                description="Min periods",
                optional=True,
                defaultValue=None
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[3], description="Output file"
            )
        )
