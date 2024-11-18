from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISSingleIlrTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "single_ilr_transform"
        self._display_name = "Single ILR transform"
        self._group = "Transformations — CoDA"
        self._group_id = "transformations_coda"
        self._short_help_string = """
            Perform a single isometric logratio transformation on the provided subcompositions.

            Returns ILR balances. Column order in input vector matters.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "subcomposition_1", "subcomposition_2", "output_vector"]

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector with compositional data.")
        self.addParameter(input_vector_param)

        subcomposition_1_param =  QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Subcomposition 1 (numerator part)",
            parentLayerParameterName=self.alg_parameters[0],
            type=QgsProcessingParameterField.Numeric,
            allowMultiple=True
        )
        subcomposition_1_param.setHelp("Names of the columns in the numerator part of the ratio.")
        self.addParameter(subcomposition_1_param)

        subcomposition_2_param = QgsProcessingParameterField(
            name=self.alg_parameters[2],
            description="Subcomposition 2 (denominator part)",
            parentLayerParameterName=self.alg_parameters[0],
            type=QgsProcessingParameterField.Numeric,
            allowMultiple=True
        )
        subcomposition_2_param.setHelp("Names of the columns in the denominator part of the ratio.")
        self.addParameter(subcomposition_2_param)

        output_vector_param =  QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[3],
            description="Output vector",
        )
        output_vector_param.setHelp("Output vector with the transformed data.")
        self.addParameter(output_vector_param)
