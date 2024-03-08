from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISLeeEnhancedFilter(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "lee_enhanced_filter"
        self._display_name = "Lee Enhanced Filter"
        self._group = "Filtering"
        self._group_id = "filtering"
        self._short_help_string = "Apply a Lee filter considering multiplicative noise components to the input raster"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "size",
            "n_looks",
            "damping_factor",
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
            E.g., 3 means a 3x3 window. Default to 3.
            '''
        )
        self.addParameter(window_size_param)

        n_looks_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Number of looks.",
            minValue=1,
            defaultValue=1,
        )
        n_looks_param.setHelp(
            '''
            Number of looks to estimate the noise variation.
            Higher values result in higher smoothing.
            Low values may result in focal mean filtering.
            Default to 1.
            '''
        )
        self.addParameter(n_looks_param)

        damping_factor = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            description="Damping factor",
            minValue=0.1,
            defaultValue=1,
            type=QgsProcessingParameterNumber.Double,
        )
        damping_factor.setHelp(
            '''
            Extent of exponential damping effect on filtering.
            Larger damping values preserve edges better but smooths less.
            Smaller values produce more smoothing.
            Default to 1.
            '''
        )
        self.addParameter(damping_factor)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[4], description="Output Raster"
        )
        output_raster_param.setHelp("The output raster data set.")
        self.addParameter(output_raster_param)
