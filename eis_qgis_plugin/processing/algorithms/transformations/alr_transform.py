from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISAlrTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "alr_transform"
        self._display_name = "ALR transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = "Perform an additive logratio transformation on the data."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "column", "keep_denominator_column", "output_vector"]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input vector"
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.alg_parameters[1],
                description="Denominator column",
                parentLayerParameterName=self.alg_parameters[0],
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                name=self.alg_parameters[2],
                description="Keep denominator column",
                defaultValue=False
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                name=self.alg_parameters[3],
                description="Output vector",
            )
        )
