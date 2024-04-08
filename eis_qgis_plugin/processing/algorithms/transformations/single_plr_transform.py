from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISSinglePlrTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "single_plr_transform"
        self._display_name = "Single PLR transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = """
            Perform a pivot logratio transformation on the selected column.

            Pivot logratio is a special case of ILR, where the numerator in the ratio is always a single \
            part and the denominator all of the parts to the right in the ordered list of parts.

            Column order in input vector matters.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "column", "output_vector"]

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector data with compositional data.")
        self.addParameter(input_vector_param)

        numerator_column = QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Numerator column",
            parentLayerParameterName=self.alg_parameters[0]
        )
        numerator_column.setHelp("The name of the numerator column to use for the transformation.")
        self.addParameter(numerator_column)

        output_vector_param = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[2],
            description="Output vector",
        )
        output_vector_param.setHelp("Output vector with the transformed data.")
        self.addParameter(output_vector_param)
