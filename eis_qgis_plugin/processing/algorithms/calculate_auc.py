from qgis.core import (
    QgsProcessingParameterMatrix,
    QgsProcessingParameterNumber,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISCalculateAuc(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "calculate_auc"
        self._display_name = "Calculate Auc"
        self._group = "Validation"  # TODO! what category does this fall under?
        self._group_id = "validation"  # Same as above.
        self._short_help_string = "Calculate area under curve (AUC)"

    def initAlgorithm(self, config=None):

        self.alg_parameters = [
            "x_values",
            "y_values",
            "auc_value",
        ]

        # Should the first 2 parameters rather be
        self.addParameter(
            QgsProcessingParameterMatrix(
                name=self.alg_parameters[0], description="X value matrix"
            )
        )

        self.addParameter(
            QgsProcessingParameterMatrix(
                name=self.alg_parameters[1], description="Y value matrix"
            )
        )

        # 
        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2], description="Result"
            )
        )