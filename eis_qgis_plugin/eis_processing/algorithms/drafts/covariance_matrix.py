from qgis.core import (
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterNumber,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISCovarianceMatrix(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "covariation_matrix"
        self._display_name = "Covariation matrix"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Compute covariance matrix on the input data."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_data", "min_periods", "delta_degrees_of_freedom", "output_file"]

        self.addParameter(
            QgsProcessingParameterFile(
                name=self.alg_parameters[0], description="Input data (numeric)"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1],
                description="Min periods",
                optional=True,
                defaultValue=None
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2],
                description="Delta degrees of freedom",
                optional=True,
                defaultValue=1
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[3], description="Output file"
            )
        )
