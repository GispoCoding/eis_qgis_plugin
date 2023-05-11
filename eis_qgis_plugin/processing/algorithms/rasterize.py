from qgis.core import (
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISRasterize(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "rasterize"
        self._display_name = "Rasterize"
        self._group = "Vector Processing"
        self._group_id = "vector_processing"
        self._short_help_string = "Rasterize a vector layer"

    def initAlgorithm(self, config=None):

        self.alg_parameters = ["input_vector", "output_raster"]

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                name=self.alg_parameters[0], description="Input vector"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[1],
                description="Output raster",
            )
        )
