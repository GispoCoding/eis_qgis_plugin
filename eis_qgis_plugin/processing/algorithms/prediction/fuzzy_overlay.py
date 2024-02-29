from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterEnum,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISFuzzyOverlay(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "fuzzy_overlay"
        self._display_name = "Fuzzy overlay"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = "Compute fuzzy overlay"

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_rasters", "overlay_method", "gamma", "output_raster"]

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                name=self.alg_parameters[0], description="Input rasters", layerType=QgsProcessing.TypeRaster
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[1],
                description="Overlay method",
                options=["And", "Or", "Sum", "Product", "Gamma"],
                defaultValue="And",
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2], description="Gamma", optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[3],
                description="Output raster",
            )
        )
