from qgis.core import (
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISSinglePlrTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "single_plr_transform"
        self._display_name = "Single PLR transform"
        self._group = "Transformations — CoDA"
        self._group_id = "transformations_coda"
        self._short_help_string = """
            Perform a pivot logratio transformation on the selected column.

            Pivot logratio is a special case of ILR, where the numerator in the ratio is always a single \
            part and the denominator all of the parts to the right in the ordered list of parts.

            Column order in input vector matters.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "numerator", "denominator", "scale", "output_vector"]

        input_vector_param = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector data with compositional data.")
        self.addParameter(input_vector_param)

        numerator_column = QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Numerator column",
            parentLayerParameterName=self.alg_parameters[0],
            type=QgsProcessingParameterField.Numeric,
        )
        numerator_column.setHelp("The name of the numerator column to use for the transformation.")
        self.addParameter(numerator_column)

        denominator_columns = QgsProcessingParameterField(
            name=self.alg_parameters[2],
            description="Denominator columns",
            parentLayerParameterName=self.alg_parameters[0],
            optional=True,
            allowMultiple=True,
        )
        denominator_columns.setHelp("The name(s) of the denominator column(s) to use for transformation.")
        self.addParameter(denominator_columns)

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

        output_vector_param = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[4],
            description="Output vector",
        )
        output_vector_param.setHelp("Output vector with the transformed data.")
        self.addParameter(output_vector_param)
