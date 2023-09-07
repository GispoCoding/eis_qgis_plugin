from qgis.core import (
    QgsProcessingParameterExtent,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterString,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm

class EISSimpleIdw(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "simple_idw"
        self._display_name = "IDW interpolation"
        self._group = "Vector processing"
        self._group_id = "vector_processing"
        self._short_help_string = "Perform inverse distance weighting (IDW) interpolation"

    def initAlgorithm(self, config=None):
        
        self.alg_parameters = [
            "input_geometries",
            "target_column",
            "resolution_x",
            "resolution_y",
            "extent",
            "power",
            "output_raster"
            ]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input geometries"
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                name=self.alg_parameters[1], description="The column name with values for each geometry"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2], description="Pixel size X"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[3], description="Pixel size Y"
            )
        )

        self.addParameter(
            QgsProcessingParameterExtent(
                name=self.alg_parameters[4], description="Raster extent", optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[5], description="Power", defaultValue=2
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[6], description="Output raster"
            )
        )
