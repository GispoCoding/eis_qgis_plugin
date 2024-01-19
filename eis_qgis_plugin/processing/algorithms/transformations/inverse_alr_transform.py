from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISInverseAlrTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "inverse_alr_transform"
        self._display_name = "Inverse ALR transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = "Perform the inverse transformation for a set of ALR transformed data."


    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "denominator_column", "scale", "output_vector"]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input vector"
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                name=self.alg_parameters[1],
                description="Denominator column name",
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2],
                description="Scale",
                defaultValue=1.0,
                type=QgsProcessingParameterNumber.Double
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                name=self.alg_parameters[3],
                description="Output vector",
            )
        )
