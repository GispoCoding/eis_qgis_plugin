from qgis.core import QgsProcessingParameterFeatureSource, QgsProcessingParameterVectorDestination

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISExtractSharedLines(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "extract_shared_lines"
        self._display_name = "Extract shared lines"
        self._group = "Vector processing"
        self._group_id = "vector_processing"
        self._short_help_string = "Extract shared lines"

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "output_vector"]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0],
                description="Input vector layer",
                # types=[QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                name=self.alg_parameters[1], description="Output"
            )
        )
