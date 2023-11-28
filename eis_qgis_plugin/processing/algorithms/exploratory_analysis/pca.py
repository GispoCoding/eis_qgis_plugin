from qgis.core import (
    QgsProcessingParameterMapLayer,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterNumber,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPca(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "pca"
        self._display_name = "Principal component analysis"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Compute PCA"

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_layer", "components", "output_file"]

        self.addParameter(
            QgsProcessingParameterMapLayer(
                name=self.alg_parameters[0], description="Input geometries"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1],
                description="Number of components",
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[2], description="Output vector"
            )
        )
