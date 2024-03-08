from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISLeeAdditiveMultiplicativeNoiseFilter(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "lee_additive_multiplicative_noise_filter"
        self._display_name = "Lee Additive Multiplicative Noise Filter"
        self._group = "Filtering"
        self._group_id = "filtering"
        self._short_help_string = '''
            Apply a Lee filter considering additive 
            and multiplicative noise components to the input raster"
            '''

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "size",
            "add_noise_var",
            "add_noise_mean",
            "multi_noise_mean",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
            )
        input_raster_param.setHelp("The input raster data set.")
        self.addParameter(input_raster_param)

        window_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Additive and Multiplicative Noise Variation",
            minValue=1,
            defaultValue=3,
        )
        window_size_param.setHelp(
            '''
            The size of the filter window.
            E.g., 3 means a 3x3 window. Default to 3.
            '''
        )
        self.addParameter(window_size_param)

        add_noise_var_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Additive Noise Variation",
            minValue=0.1,
            defaultValue=0.25,
            type=QgsProcessingParameterNumber.Double,
        )
        add_noise_var_param.setHelp("The additive noise variation. Default to 0.25.")
        self.addParameter(add_noise_var_param)

        add_noise_mean_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            description="Additive Noise Mean",
            defaultValue=0,
            type=QgsProcessingParameterNumber.Double,
        )
        add_noise_mean_param.setHelp("The additive noise mean. Default to 0.")
        self.addParameter(add_noise_mean_param)

        mult_noise_mean_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4],
            description="Multiplicative Noise Mean",
            minValue=0.1,
            defaultValue=1.0,
            type=QgsProcessingParameterNumber.Double,
        )
        mult_noise_mean_param.setHelp("The multiplicative noise mean. Default to 1.")
        self.addParameter(mult_noise_mean_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[5], description="Output Raster"
        )
        output_raster_param.setHelp("The output raster data set.")
        self.addParameter(output_raster_param)
