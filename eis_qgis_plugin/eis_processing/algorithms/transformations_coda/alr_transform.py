from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISAlrTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "alr_transform"
        self._display_name = "ALR transform"
        self._group = "Transformations — CoDA"
        self._group_id = "transformations_coda"
        self._short_help_string = "Perform an additive logratio transformation on the data."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "column", "keep_denominator_column", "output_vector"]

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector with compositional data.")
        self.addParameter(input_vector_param)

        denominator_column_param = QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Denominator column",
            parentLayerParameterName=self.alg_parameters[0],
            optional=True,
        )
        denominator_column_param.setHelp("The column to be used as the denominator column.")
        self.addParameter(denominator_column_param)

        keep_denominator_column_param = QgsProcessingParameterBoolean(
            name=self.alg_parameters[2],
            description="Keep denominator column",
            defaultValue=False
        )
        keep_denominator_column_param.setHelp(
            "Whether to include the used denominator column in the result."
        )
        self.addParameter(keep_denominator_column_param)

        output_vector_param = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[3],
            description="Output vector",
        )
        output_vector_param.setHelp("Output vector with the ALR transformed data.")
        self.addParameter(output_vector_param)
