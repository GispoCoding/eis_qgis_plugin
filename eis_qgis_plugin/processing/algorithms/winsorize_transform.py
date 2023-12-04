from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISWinsorizeTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "winsorize_transform"
        self._display_name = "Winsorize transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = "Winsorize data based on specified percentile values."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "percentile_lower",
            "percentile_higher",
            "inside",
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
                description="Lower percentile",
                type=QgsProcessingParameterNumber.Double,
                minValue=0.0,
                maxValue=100.0,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2],
                description="Higher percentile",
                type=QgsProcessingParameterNumber.Double,
                minValue=0.0,
                maxValue=100.0,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                name=self.alg_parameters[3], description="Inside", defaultValue=False
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[4], description="Output raster"
            )
        )
