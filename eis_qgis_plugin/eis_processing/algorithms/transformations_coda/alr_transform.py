from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterVectorLayer,
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
        self.alg_parameters = [
            "input_vector", "columns", "denominator_column", "keep_denominator_column", "scale", "output_vector"
        ]

        input_vector_param = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input data.")
        self.addParameter(input_vector_param)

        columns_param = QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Columns",
            parentLayerParameterName=self.alg_parameters[0],
            optional=True,
            allowMultiple=True,
        )
        columns_param.setHelp("Columns to be transformed.")
        self.addParameter(columns_param)

        denominator_column_param = QgsProcessingParameterField(
            name=self.alg_parameters[2],
            description="Denominator column",
            parentLayerParameterName=self.alg_parameters[0],
            type=QgsProcessingParameterField.Numeric,
            optional=True,
        )
        denominator_column_param.setHelp("The column to be used as the denominator column.")
        self.addParameter(denominator_column_param)

        keep_denominator_column_param = QgsProcessingParameterBoolean(
            name=self.alg_parameters[3],
            description="Keep denominator column",
            defaultValue=False
        )
        keep_denominator_column_param.setHelp(
            "Whether to include the used denominator column in the result."
        )
        self.addParameter(keep_denominator_column_param)

        scale_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4],
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
            name=self.alg_parameters[5],
            description="Output vector",
        )
        output_vector_param.setHelp("Output vector with the ALR transformed data.")
        self.addParameter(output_vector_param)
