from qgis.core import (
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISClipTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "clip_transform"
        self._display_name = "Clip transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = (
            "Clips data based on specified upper and lower limits."
        )

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "limit_lower",
            "limit_higher",
            "output_raster",
        ]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1],
                description="Lower",
                type=QgsProcessingParameterNumber.Double,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2],
                description="Higher",
                type=QgsProcessingParameterNumber.Double,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[3], description="Output raster"
            )
        )
