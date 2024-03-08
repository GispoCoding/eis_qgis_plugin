from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISLeeMultiplicativeNoiseFilter(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "lee_multiplicative_noise_filter"
        self._display_name = "Lee multiplicative noise filter"
        self._group = "Filtering"
        self._group_id = "filtering"
        self._short_help_string = "Apply a Lee filter considering multiplicative noise components to the input raster"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "size",
            "multi_noise_mean",
            "n_looks",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        input_raster_param.setHelp("The input raster data set.")
        self.addParameter(input_raster_param)

        window_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Size",
            minValue=1,
            defaultValue=3,
        )
        window_size_param.setHelp(
            '''
            The size of the filter window.
            E.g., 3 means a 3x3 window.
            '''
        )
        self.addParameter(window_size_param)

        noise_var_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Multiplicative Noise Variation",
            minValue=1,
            defaultValue=3,
        )
        noise_var_param.setHelp(
            '''
            The size of the filter window.
            E.g., 3 means a 3x3 window.
            '''
        )
        self.addParameter(noise_var_param)

        n_looks_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            description="Number of looks",
            minValue=1,
            defaultValue=1,
        )
        n_looks_param.setHelp(
            '''
            Number of looks to estimate the noise variation.
            Higher values result in higher smoothing.
            Low values may result in focal mean filtering.
            '''
        )
        self.addParameter(n_looks_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[4], description="Output raster"
        )
        output_raster_param.setHelp("The output raster data set.")
        self.addParameter(output_raster_param)
