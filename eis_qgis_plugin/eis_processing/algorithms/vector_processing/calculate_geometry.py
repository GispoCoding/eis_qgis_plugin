from qgis.core import QgsProcessing, QgsProcessingParameterVectorDestination, QgsProcessingParameterVectorLayer

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


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

        input_vector_param = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[0],
            description="Input vector",
            types=[QgsProcessing.TypeVectorPolygon, QgsProcessing.TypeVectorLine]
        )
        input_vector_param.setHelp("Input vector file with line or polygon features.")
        self.addParameter(input_vector_param)

        output_vector = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[1], description="Output vector"
        )
        output_vector.setHelp("Output vector with calculation results.")
        self.addParameter(output_vector)
