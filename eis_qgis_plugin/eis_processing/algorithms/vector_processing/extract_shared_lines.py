from qgis.core import QgsProcessing, QgsProcessingParameterVectorDestination, QgsProcessingParameterVectorLayer

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISExtractSharedLines(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "extract_shared_lines"
        self._display_name = "Extract shared lines"
        self._group = "Vector processing"
        self._group_id = "vector_processing"
        self._short_help_string = "Extract shared lines between polygon features."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "output_vector"]

        input_vector_param = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[0],
            description="Input vector",
            types=[QgsProcessing.TypeVectorPolygon]
        )
        input_vector_param.setHelp("Input vector with polygon features.")
        self.addParameter(input_vector_param)

        output_vector_param = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[1], description="Extract shared lines output"
        )
        output_vector_param.setHelp("Output vector layer with the shared lines.")
        self.addParameter(output_vector_param)
