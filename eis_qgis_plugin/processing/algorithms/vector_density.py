from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISVectorDensity(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()
    
        self._name = "vector_density"
        self._display_name = "Vector density"
        self._group = "Vector processing"
        self._group_id = "vector_processing"
        self._short_help_string = "Compute density of geometries within raster"

    def initAlgorithm(self, config=None):
        
        self.alg_parameters = [
            "input_vectors",
            "resolution",
            "raster_profile",
            "buffer_value",
            "output_raster"
        ]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input vectors"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1], description="Cell size"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[2], description="Raster profile"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[3], description="Buffer"
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[4], description="Output vector data and metadata"
            )
        )
