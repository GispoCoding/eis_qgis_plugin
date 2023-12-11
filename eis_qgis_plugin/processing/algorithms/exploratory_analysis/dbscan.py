from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterNumber,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISDbscan(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "dbscan"
        self._display_name = "DBSCAN"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Perform DBSCAN"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_vector",
            "max_distance",
            "min_samples",
            "output_vector",
        ]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input vector"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1], description="Maximum distance"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2], description="Minimum number of samples"
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[3], description="Output vector"
            )
        )
