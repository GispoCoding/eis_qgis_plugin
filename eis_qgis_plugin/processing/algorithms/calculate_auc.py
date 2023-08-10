from qgis.core import (
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISCalculateAuc(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "calculate_auc"
        self._display_name = "Calculate AUC"
        self._group = "Validation"
        self._group_id = "validation"
        self._short_help_string = "Calculate area under curve (AUC)"

    def initAlgorithm(self, config=None):
        # TODO: Give input data in some other form? At least, not as several files.
        self.alg_parameters = [
            "x_values",
            "y_values",
            "output_file"
        ]

        self.addParameter(
            QgsProcessingParameterFile(
                name=self.alg_parameters[0], description="X-value matrix"
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                name=self.alg_parameters[1], description="Y-value matrix"
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[2],
                description="Output file",
            )
        )