from qgis.core import (
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPlotPredictionAreaCurve(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "plot_prediction_area_curve"
        self._display_name = "Plot prediction area curve"
        self._group = "Validation"
        self._group_id = "validation"
        self._short_help_string = "Plot prediction-area (P-A) curve"

    def initAlgorithm(self, config=None):
        # TODO: Give input data in some other form? At least, not as several files.
        self.alg_parameters = [
            "true_positive_rate_values",
            "proportion_of_area_values",
            "threshold_values",
            "plot_figure",
        ]

        self.addParameter(
            QgsProcessingParameterFile(
                name=self.alg_parameters[0], description="True positive rate values"
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                name=self.alg_parameters[1], description="Proportion of area values"
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                name=self.alg_parameters[2], description="Threshold values"
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[3], description="Output plot figure"
            )
        )
