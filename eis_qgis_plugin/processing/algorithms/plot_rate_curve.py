from qgis.core import (
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterString,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPlotRateCurve(EISProcessingAlgorithm):

    def __init__(self) -> None:
        super().__init__()

        self._name = "plot_rate_curve"
        self._display_name = "Plot rate curve"
        self._group = "Validation"
        self._group_id = "validation"
        self._short_help_string = "Plot success rate, prediction rate or ROC curve"

    def initAlgorithm(self, config=None):
        
        self.alg_parameters = ["x_values", "y_values", "plot_type", "plot_figure"]

        self.addParameter(
            QgsProcessingParameterFile(
                name=self.alg_parameters[0], description="False positive rate or proportion of area"
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                name=self.alg_parameters[1], description="True positive rate"
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                name=self.alg_parameters[2], description="Plot type"
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[3], description="Output plot figure"
            )
        )
