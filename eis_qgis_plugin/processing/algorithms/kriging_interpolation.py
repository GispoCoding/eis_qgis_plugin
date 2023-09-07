from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterExtent,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterString,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm

class EISKrigingInterpolation(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "kriging_interpolation"
        self._display_name = "Kriging interpolation"
        self._group = "Vector processing"
        self._group_id = "vector_processing"
        self._short_help_string = "Perform kriging interpolation"

    def initAlgorithm(self, config=None):
        
        self.alg_parameters = [
            "input_geometries",
            "target_column",
            "resolution_x",
            "resolution_y",
            "extent",
            "variogram_model",
            "coordinates_type",
            "method",
            "drift_terms",
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
            QgsProcessingParameterEnum(
                name=self.alg_parameters[5],
                description="Variogram model",
                options=["linear", "power", "gaussian", "spherical", "exponential", "hole-effect"],
                defaultValue="linear"
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[6],
                description="Coordinates type",
                options=["euclidean", "geographic"],
                defaultValue="geographic"
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[7],
                description="Kriging method",
                options=["ordinary", "universal"],
                defaultValue="ordinary"
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                name=self.alg_parameters[8],
                description="Drift terms",
                multiLine=True,
                defaultValue="regional_linear"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[9],
                description="Output raster and metadata",
            )
        )
