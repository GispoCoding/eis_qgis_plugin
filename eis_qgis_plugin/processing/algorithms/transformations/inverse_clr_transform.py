from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


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

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input vector"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1],
                description="Scale",
                defaultValue=1.0,
                type=QgsProcessingParameterNumber.Double
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                name=self.alg_parameters[2],
                description="Output vector",
            )
        )
