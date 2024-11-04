from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISInverseAlrTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "inverse_alr_transform"
        self._display_name = "Inverse ALR transform"
        self._group = "Transformations — CoDA"
        self._group_id = "transformations_coda"
        self._short_help_string = "Perform the inverse transformation for a set of ALR transformed data."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "denominator_column", "scale", "output_vector"]

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector with ALR transformed compositional data.")
        self.addParameter(input_vector_param)

        denominator_column_name_param = QgsProcessingParameterString(
            name=self.alg_parameters[1],
            description="Denominator column name",
        )
        denominator_column_name_param.setHelp("The name of the denominator column.")
        self.addParameter(denominator_column_name_param)

        scale_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Scale",
            defaultValue=1.0,
            type=QgsProcessingParameterNumber.Double
        )
        scale_param.setHelp(
            "The value to which each composition should be normalized. \
            Eg., if the composition is expressed as percentages, scale=100."
        )
        self.addParameter(scale_param)

        output_vector_param = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[3],
            description="Output vector",
        )
        output_vector_param.setHelp("Output vector with inverse transformed data.")
        self.addParameter(output_vector_param)
