from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISSingleIlrTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "single_ilr_transform"
        self._display_name = "Single ILR transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = "Perform a single isometric logratio transformation on the provided subcompositions."


    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "subcomposition_1", "subcomposition_2", "output_vector"]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input vector"
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.alg_parameters[1],
                description="Subcomposition 1 (numerator part)",
                parentLayerParameterName=self.alg_parameters[0],
                allowMultiple=True
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.alg_parameters[2],
                description="Subcomposition 2 (denominator part)",
                parentLayerParameterName=self.alg_parameters[0],
                allowMultiple=True
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                name=self.alg_parameters[3],
                description="Output vector",
            )
        )
