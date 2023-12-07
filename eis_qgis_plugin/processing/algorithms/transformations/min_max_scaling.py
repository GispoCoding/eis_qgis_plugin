from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISMinMaxScaling(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "min_max_scaling"
        self._display_name = "Min-max scale"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = (
            "Normalize raster to specified range using min and max values"
        )

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "min", "max", "output_raster"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1],
                description="Min",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2],
                description="Max",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=1.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[3], description="Output raster"
            )
        )
