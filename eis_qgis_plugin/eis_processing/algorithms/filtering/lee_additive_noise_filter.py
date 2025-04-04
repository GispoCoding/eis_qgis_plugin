from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISLeeAdditiveNoiseFilter(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "lee_additive_noise_filter"
        self._display_name = "Lee additive noise filter"
        self._group = "Filtering"
        self._group_id = "filtering"
        self._short_help_string = "Apply a Lee filter considering additive noise components to the input raster"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "size",
            "add_noise_var",
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
            minValue=3,
            defaultValue=3,
        )
        window_size_param.setHelp(
            '''
            The size of the filter window. 
            E.g., 3 means a 3x3 window. 
            Only odd numbers are allowed.
            '''
        )
        self.addParameter(window_size_param)

        add_noise_var_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Additive Noise Variation",
            defaultValue=0.25,
            minValue=0,
            type=QgsProcessingParameterNumber.Double,
        )
        add_noise_var_param.setHelp("The additive noise variation.")
        self.addParameter(add_noise_var_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Lee additive noise filter output"
        )
        output_raster_param.setHelp("The output raster data set.")
        self.addParameter(output_raster_param)
