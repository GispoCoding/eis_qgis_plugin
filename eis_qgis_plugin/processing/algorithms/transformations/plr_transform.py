from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPlrTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "plr_transform"
        self._display_name = "Pairwise logratio transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = (
            "Perform a pivot logratio transformation on the dataframe, returning the full set of transforms."
        )


    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "output_vector"]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input vector"
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                name=self.alg_parameters[1],
                description="Output vector",
            )
        )
