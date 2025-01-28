from qgis.core import (
    QgsProcessingParameterField,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPairwiseLogratio(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "pairwise_logratio"
        self._display_name = "Pairwise logratio transform"
        self._group = "Transformations — CoDA"
        self._group_id = "transformations_coda"
        self._short_help_string = "Perform a pairwise logratio transformation on the given columns."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "numerator_column", "denominator_column", "output_vector"]

        input_vector_param = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector with compositional data.")
        self.addParameter(input_vector_param)

        numerator_column_param = QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Numerator column",
            parentLayerParameterName=self.alg_parameters[0],
            type=QgsProcessingParameterField.Numeric,
        )
        numerator_column_param.setHelp("Name of the column to use as the numerator column.")
        self.addParameter(numerator_column_param)

        denominator_column_param = QgsProcessingParameterField(
            name=self.alg_parameters[2],
            description="Denominator column",
            parentLayerParameterName=self.alg_parameters[0],
            type=QgsProcessingParameterField.Numeric,
        )
        denominator_column_param.setHelp("Name of the column to use as the denominator column.")
        self.addParameter(denominator_column_param)

        output_vector_param = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[3],
            description="Pairwise logratio transform output",
        )
        output_vector_param.setHelp("Output vector with the transformed values.")
        self.addParameter(output_vector_param)
