from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterString,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISRasterize(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "rasterize"
        self._display_name = "Rasterize"
        self._group = "Vector Processing"
        self._group_id = "vector_processing"
        self._short_help_string = "Rasterize a vector layer"

    def initAlgorithm(self, config=None):

        self.alg_parameters = ["input_vector",
                                "resolution",
                                "value_column",
                                "default_value",
                                "fill_value",
                                "base_raster_profile_raster",
                                "buffer_value",
                                "merge_strategy",
                                "output_raster"]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input vector"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name = self.alg_parameters[1], description="Resolution", optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                name=self.alg_parameters[2], description="Column name", optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[3], description="Default value", defaultValue=1.0
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[4], description="Fill value", defaultValue=0.0
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[5], description="Base raster for raster profile", optional=True
            )
        )
        
        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[6], description="Buffer value", optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[7], description="Merge strategy", options=["replace", "add"],
                defaultValue="replace"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(name=self.alg_parameters[8], description="Output raster"
            )
        )
