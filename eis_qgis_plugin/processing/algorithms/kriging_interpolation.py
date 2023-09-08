from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterExtent,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
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
            QgsProcessingParameterField(
                name=self.alg_parameters[1],
                description="Interpolation attribute",
                parentLayerParameterName=self.alg_parameters[0]
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
            QgsProcessingParameterEnum(
                name=self.alg_parameters[8],
                description="Drift terms",
                options=["regional_linear", "point_log", "external_Z", "specified", "functional"],
                defaultValue="regional_linear",
                allowMultiple=True
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[9],
                description="Output raster",
            )
        )