from qgis.core import (
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterNumber
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISBinarize(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "binarize"
        self._display_name = "Binarize"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = "Calculate binarize transformation for data"

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "threshold", "output_raster"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1], description="Binarizing threshold"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[2],
                description="Output raster",
            )
        )
