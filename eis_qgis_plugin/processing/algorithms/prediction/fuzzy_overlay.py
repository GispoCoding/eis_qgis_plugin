from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
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
        self.alg_parameters = ["input_layer", "fuzzy_method", "gamma", "output_raster"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input layer"
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[1],
                description="Fuzzy method",
                options=["And", "Or", "Sum", "Product", "Gamma"],
                defaultValue="And",
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2], description="gamma", optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[3],
                description="Output raster",
            )
        )
