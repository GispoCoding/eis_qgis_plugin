from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPairwiseLogratio(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "pairwise_logratio"
        self._display_name = "Pairwise logratio transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = "Perform a pairwise logratio transformation on the given columns."


    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "numerator_column", "denominator_column", "output_vector"]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input vector"
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.alg_parameters[1],
                description="Numerator column",
                parentLayerParameterName=self.alg_parameters[0],
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.alg_parameters[2],
                description="Denominator column",
                parentLayerParameterName=self.alg_parameters[0],
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                name=self.alg_parameters[3],
                description="Output vector",
            )
        )
