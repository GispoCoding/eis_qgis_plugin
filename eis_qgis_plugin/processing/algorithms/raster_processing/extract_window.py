from qgis.core import (
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterPoint,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISExtractWindow(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "extract_window"
        self._display_name = "Extract window"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Extract window from raster"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "center_coords",
            "height",
            "width",
            "output_raster",
        ]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        )
        self.addParameter(
            QgsProcessingParameterPoint(
                name=self.alg_parameters[1], description="Center coordinates"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2], description="Height"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[3], description="Width"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[4], description="Output raster"
            )
        )
