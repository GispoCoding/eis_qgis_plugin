from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterCrs,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
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
            "template_raster", "constant_value", "coord_west", "coord_north",
            "coord_east", "coord_south", "target_epsg", "target_pixel_size",
            "raster_width", "raster_height", "nodata_value", "out_raster"
            ]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0],
                description="Template raster",
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1],
                description="Constant value to use.",
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2],
                description="West coordinate",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[3],
                description="North coordinate",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[4],
                description="East coordinate",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[5],
                description="South coordinate",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterCrs(
                name=self.alg_parameters[6],
                description="Target CRS",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[7],
                description="Target pixel size",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[8],
                description="Raster width",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[9],
                description="Raster height",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[10],
                description="Nodata value",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[11], description="out_raster",
            )
        )
