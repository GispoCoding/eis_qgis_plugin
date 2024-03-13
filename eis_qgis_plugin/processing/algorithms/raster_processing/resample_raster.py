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
        self._short_help_string = "Resample raster to a new resolution."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "resolution",
            "resampling_method",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("Input raster to be resampled.")
        self.addParameter(input_raster_param)

        target_pixel_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Target pixel size",
            type=QgsProcessingParameterNumber.Double,
        )
        target_pixel_size_param.setHelp("The pixel size / resolution in the output raster.")
        self.addParameter(target_pixel_size_param)

        resampling_method_param = QgsProcessingParameterEnum(
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
            defaultValue="Nearest",
        )
        resampling_method_param.setHelp("The resampling method.")
        self.addParameter(resampling_method_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Output raster"
        )
        output_raster_param.setHelp("Output resampled raster.")
        self.addParameter(output_raster_param)
