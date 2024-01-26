from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISResampleRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "resample_raster"
        self._display_name = "Resample raster"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Resample raster to a new resolution"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "resolution",
            "resampling_method",
            "output_raster",
        ]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1],
                description="Resolution",
                type=QgsProcessingParameterNumber.Double,
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[2],
                description="Resampling method",
                options=[
                    "Nearest",
                    "Bilinear",
                    "Cubic",
                    "Average",
                    "Gauss",
                    "Max",
                    "Min",
                ],
                defaultValue="Bilinear",
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[3], description="Output raster"
            )
        )
