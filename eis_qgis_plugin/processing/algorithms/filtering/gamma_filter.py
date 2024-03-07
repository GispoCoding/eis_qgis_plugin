from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm

from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)



class EISGammaFilter(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "gamma_filter"
        self._display_name = "Gamma Filter"
        self._group = "Filtering"
        self._group_id = "filtering"
        self._short_help_string = '''
            Apply a Gamma filter to the input raster.
            Higher number of looks result in better edge preservation.
            '''

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "size",
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
            minValue=0.1,
            defaultValue=1,
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
            description="Gamma Noise Variation",
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

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Output Raster"
        )
        output_raster_param.setHelp("The output raster data set.")
        self.addParameter(output_raster_param)
