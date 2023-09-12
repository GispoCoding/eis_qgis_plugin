from qgis.core import (
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterMapLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISDescriptiveStatistics(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "descriptive_statistics"
        self._display_name = "Descriptive statistics"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Generate descriptive statistics for a layer"

    def initAlgorithm(self, config=None):

        self.alg_parameters = ["input_layer", "output_file"]

        self.addParameter(
            QgsProcessingParameterMapLayer(
                name=self.alg_parameters[0], description="Input layer"
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[1],
                description="Output file",
            )
        )
