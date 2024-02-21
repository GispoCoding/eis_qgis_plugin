from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISClassifyAspect(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "classify_aspect"
        self._display_name = "Classify aspect"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Classify an aspect raster data set."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "output_raster",
            "unit",
            "num_classes"
        ]
    
        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("The input raster data set.")
        self.addParameter(input_raster_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[1], description="Output raster"
        )
        output_raster_param.setHelp("The output raster data set.")
        self.addParameter(output_raster_param)

        unit_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[2],
            options=["degrees", "radians"],
            defaultValue="radians",
            description="Unit",
        )
        unit_param.setHelp("The unit of the input raster. Defaults to radians.")
        self.addParameter(unit_param)

        num_classes_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[3],
            options=["8", "16"],
            defaultValue="8",
            description="Number of classes",
        )
        num_classes_param.setHelp("The number of classes for discretization. Either 8 or 16 classes allowed.")
        self.addParameter(num_classes_param)