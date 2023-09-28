from qgis.core import (
    QgsProcessingParameterExtent,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISIdwInterpolation(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "idw_interpolation"
        self._display_name = "IDW interpolation"
        self._group = "Vector processing"
        self._group_id = "vector_processing"
        self._short_help_string = (
            "Perform inverse distance weighting (IDW) interpolation"
        )

    def initAlgorithm(self, config=None):

        self.alg_parameters = [
            "input_vector",
            "target_column",
            "resolution",
            "extent",
            "power",
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
            QgsProcessingParameterNumber(
                name=self.alg_parameters[4], description="Power", defaultValue=2
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[5], description="Output raster"
            )
        )
