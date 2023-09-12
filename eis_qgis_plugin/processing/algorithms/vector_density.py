from qgis.core import (
    QgsProcessingParameterEnum,
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
            "statistic",
            "output_raster",
        ]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input vectors"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1], description="Cell size", optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[2], description="Raster profile", optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[3], description="Buffer", optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[4],
                description="Statistic",
                options=["density", "count"],
                defaultValue="density",
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[5],
                description="Output vector data and metadata",
            )
        )
