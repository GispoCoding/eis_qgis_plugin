from qgis.core import (
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISSigmoidTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "sigmoid_transform"
        self._display_name = "Sigmoid transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = (
            "Transform data into a sigmoid-shape based on a specified new range"
        )

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "limit_lower",
            "limit_upper",
            "slope",
            "center",
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
                defaultValue=0.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2],
                description="Upper",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=1.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[3],
                description="Slope",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=1.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                name=self.alg_parameters[4], description="Center", defaultValue=True
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[5], description="Output raster"
            )
        )
