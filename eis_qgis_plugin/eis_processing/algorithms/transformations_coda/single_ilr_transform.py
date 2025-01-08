from qgis.core import (
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterVectorLayer,
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
        self.alg_parameters = ["input_vector", "subcomposition_1", "subcomposition_2", "scale", "output_vector"]

        input_vector_param = QgsProcessingParameterVectorLayer(
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

        scale_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            description="Scale",
            optional=True
        )
        scale_param.setHelp(
            "The value to which each composition should be normalized. \
            Eg., if the composition is expressed as percentages, scale=100. \
            Leave empty if data is already closed."
        )
        self.addParameter(scale_param)

        output_vector_param =  QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[4],
            description="Output vector",
        )
        output_vector_param.setHelp("Output vector with the transformed data.")
        self.addParameter(output_vector_param)
