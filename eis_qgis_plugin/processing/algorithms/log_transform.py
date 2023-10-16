from qgis.core import (
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterEnum,
    QgsProcessingParameterRasterDestination
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISLogTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "log_transform"
        self._display_name = "Logarithmic transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = "Perform a logarithmic transformation on the provided data."

    def initAlgorithm(self, config=None):

        self.alg_parameters = ["input_raster", "log_type", "output_raster"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[1],
                description="Lower",
                options=["log2", "log10", "ln"]
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[2], description="Output raster"
            )
        )
