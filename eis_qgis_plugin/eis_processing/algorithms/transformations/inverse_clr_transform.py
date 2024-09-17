from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISInverseClrTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "inverse_clr_transform"
        self._display_name = "Inverse CLR transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = "Perform the inverse transformation for a set of CLR transformed data."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "scale", "output_vector"]  # NOTE: Colnames param omitted

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector with CLR transformed compositional data.")
        self.addParameter(input_vector_param)

        scale_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
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
            name=self.alg_parameters[2],
            description="Output vector",
        )
        output_vector_param.setHelp("Output vector with inverse transformed data.")
        self.addParameter(output_vector_param)

