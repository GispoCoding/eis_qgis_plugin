from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterExtent,
    QgsProcessingParameterCrs,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISCreateConstantRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "create_constant_raster"
        self._display_name = "Create constant raster"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Create a constant raster based on a user-defined value."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "extent", "target_crs", "pixel_size", "constant_value", "out_raster"
            ]

        self.addParameter(
            QgsProcessingParameterExtent(
                name=self.alg_parameters[0],
                description="Extent",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterCrs(
                name=self.alg_parameters[1],
                description="Target CRS",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2],
                description="Target pixel size",
                # optional=True,
                defaultValue=0.01
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[3],
                description="Constant value to use.",
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[4], description="out_raster",
            )
        )
