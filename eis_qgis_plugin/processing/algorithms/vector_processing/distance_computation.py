from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISDistanceComputation(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "distance_computation"
        self._display_name = "Distance computation"
        self._group = "Vector processing"
        self._group_id = "vector_processing"
        self._short_help_string = "Calculate distance from raster cell to nearest geometry."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "geometries", "output_raster"]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp(
            "Input raster used to determine raster metadata (transform) of the output distance raster."
        )
        self.addParameter(input_raster_param)

        geometries_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[1], description="Geometries"
        )
        geometries_param.setHelp("The geometries to determine distance to.")
        self.addParameter(geometries_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[2], description="Output raster"
        )
        output_raster_param.setHelp("Output distance raster.")
        self.addParameter(output_raster_param)
