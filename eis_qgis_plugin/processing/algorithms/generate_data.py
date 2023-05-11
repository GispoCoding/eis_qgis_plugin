from qgis.core import (
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISGenerateData(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "generate_data"
        self._display_name = "Generate training data"
        self._group = "Modelling"
        self._group_id = "modelling"
        self._short_help_string = "Generate training data for machine learning tools"

    def initAlgorithm(self, config=None):

        self.alg_parameters = ["input_layer", "output_file"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input layer"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[1],
                description="Output file",
            )
        )
