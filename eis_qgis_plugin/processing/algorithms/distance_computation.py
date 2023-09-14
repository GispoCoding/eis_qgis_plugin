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
        self._display_name = "Distance computation (R)"
        self._group = "Spatial analysis"
        self._group_id = "spatial_analysis"
        self._short_help_string = "Compute distance"

    def initAlgorithm(self, config=None):
        
        self.alg_parameters = ["input_raster", "geometries", "output_raster"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[1], description="Geometries"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[2], description="Output raster (distances)"
            )
        )
