from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISClassifyAspect(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "classify aspect"
        self._display_name = "Classify Aspect"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Classify an aspect raster data set."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["raster", "unit", "num_classes"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[1],
                options=["degrees", "radians"],
                defaultValue="radians",
                description="The unit of the input raster.",
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[2],
                options=[8, 16],
                defaultValue=8,
                description="The number of classes for discretization. Either 8 or 16 classes allowed.",
            )
        )