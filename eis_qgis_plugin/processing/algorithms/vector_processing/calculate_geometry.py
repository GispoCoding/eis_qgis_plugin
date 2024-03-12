from qgis.core import QgsProcessingParameterFeatureSource, QgsProcessingParameterVectorDestination

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISCalculateGeometry(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "calculate_geometry"
        self._display_name = "Calculate geometry"
        self._group = "Vector processing"
        self._group_id = "vector_processing"
        self._short_help_string = "Calculate vector geometry (length, area) for lines and polygons."

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
