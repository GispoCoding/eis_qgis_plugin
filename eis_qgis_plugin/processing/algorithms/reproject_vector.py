from qgis.core import (
    QgsProcessingParameterCrs,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm

class EISReprojectVector(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "reproject_vector"
        self._display_name = "Reproject vector"
        self._group = "Vector Processing"
        self._group_id = "vector_processing"
        self._short_help_string = "Reproject a vector layer"

    def initAlgorithm(self, config=None):
        
        self.alg_parameters = ["input_vector", "target_crs", "output_vector"]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input vector"
            )
        )

        self.addParameter(
            QgsProcessingParameterCrs(
                name=self.alg_parameters[1], description="Target crs"
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                name=self.alg_parameters[2], description="Output vector"
            )
        )
