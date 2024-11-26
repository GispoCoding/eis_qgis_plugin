from qgis.core import (
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISExtractValuesFromRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "extract_values_from_raster"
        self._display_name = "Extract values from raster (WIP)"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Extract values from raster. To be refactored."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "geometries",
            "output_vector",
        ]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0],
                description="Input raster",
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                name=self.alg_parameters[1], description="Extraction locations"
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                name=self.alg_parameters[2], description="Output vector"
            )
        )
