from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterExtent,
    QgsProcessingParameterEnum,
    QgsProcessingParameterString
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
            "pixel_size_x",
            "pixel_size_y",
            "extent",
            "variogram_model",
            "method",
            "drift_terms",
            "output_raster"
        ]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input vector"
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.alg_parameters[1], description="Target column/field", parentLayerParameterName="input_vector"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2],
                description="Pixel size x",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.1
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[3],
                description="Pixel size y",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.1
            )
        )

        self.addParameter(
            QgsProcessingParameterExtent(
                name=self.alg_parameters[4], description="Extent", optional=True
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
                description="Method",
                options=["ordinary", "universal"],
                defaultValue="ordinary"
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                name=self.alg_parameters[7], description="Drift terms", defaultValue="regional_linear"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[8], description="Output raster"
            )
        )
