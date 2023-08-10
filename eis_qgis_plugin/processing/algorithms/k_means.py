from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterNumber,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISKMeans(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "k_means"
        self._display_name = "K-means clustering"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Perform K-means clustering"

    def initAlgorithm(self, config=None):
        
        self.alg_parameters = [
            "input_geometries",
            "clusters",
            "random_state",
            "output_file"
        ]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input geometries"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1], description="Number of clusters", optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2], description="Random state", optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[3], description="Output file"
            )
        )
