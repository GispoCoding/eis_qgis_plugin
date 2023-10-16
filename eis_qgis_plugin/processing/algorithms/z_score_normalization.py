from qgis.core import (
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterRasterDestination
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISZScoreNormalization(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "z_score_normalization"
        self._display_name = "Z score normalization"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = "Normalize data based on mean and standard deviation."

    def initAlgorithm(self, config=None):

        self.alg_parameters = ["input_raster", "output_raster"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[1], description="Output raster"
            )
        )
