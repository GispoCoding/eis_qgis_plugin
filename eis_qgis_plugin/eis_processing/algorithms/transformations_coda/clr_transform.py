from qgis.core import (
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISClrTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "clr_transform"
        self._display_name = "CLR transform"
        self._group = "Transformations — CoDA"
        self._group_id = "transformations_coda"
        self._short_help_string = "Perform a centered logratio transformation on the data."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "output_vector"]

        input_vector_param = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector with compositional data.")
        self.addParameter(input_vector_param)

        output_vector_param = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[1],
            description="CLR transform output",
        )
        output_vector_param.setHelp("Output vector with the CLR transformed data.")
        self.addParameter(output_vector_param)
