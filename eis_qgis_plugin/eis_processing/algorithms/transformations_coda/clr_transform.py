from qgis.core import (
    QgsProcessingParameterField,
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
        self.alg_parameters = ["input_vector", "columns", "output_vector"]

        input_vector_param = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector with compositional data.")
        self.addParameter(input_vector_param)

        columns_param = QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Columns",
            parentLayerParameterName=self.alg_parameters[0],
            optional=True,
            allowMultiple=True
        )
        columns_param.setHelp("The names of the columns to be transformed.")
        self.addParameter(columns_param)

        output_vector_param = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[2],
            description="Output vector",
        )
        output_vector_param.setHelp("Output vector with the CLR transformed data.")
        self.addParameter(output_vector_param)
