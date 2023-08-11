from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISDistanceComputation(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "distance_computation"
        self._display_name = "Distance computation"
        self._group = "Spatial analysis"
        self._group_id = "spatial_analysis"
        self._short_help_string = "Compute distance"

    def initAlgorithm(self, config=None):
        
        self.alg_parameters = ["raster_profile", "geometries", "output_array"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster profile"
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[1], description="Geometries"
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[2], description="Output distances"
            )
        )
