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
            "input_vector",
            "target_column",
            "resolution",
            "extent",
            "variogram_model",
            "coordinates_type",
            "method",
            "output_raster",
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
                parentLayerParameterName=self.alg_parameters[0],
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2], description="Pixel size"
            )
        )

        self.addParameter(
            QgsProcessingParameterExtent(
                name=self.alg_parameters[3], description="Raster extent", optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[4],
                description="Variogram model",
                options=["linear", "power", "gaussian", "spherical", "exponential"],
                defaultValue="linear",
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[5],
                description="Coordinates type",
                options=["geographic", "euclidean"],
                defaultValue="geographic",
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[6],
                description="Kriging method",
                options=["ordinary", "universal"],
                defaultValue="ordinary",
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[7],
                description="Output raster",
            )
        )
