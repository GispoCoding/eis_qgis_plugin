from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISSinglePlrTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "single_plr_transform"
        self._display_name = "Single PLR transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = "Perform a pivot logratio transformation on the selected column."


    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "column", "output_vector"]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input vector"
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.alg_parameters[1],
                description="Numerator column",
                parentLayerParameterName=self.alg_parameters[0]
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                name=self.alg_parameters[2],
                description="Output vector",
            )
        )
