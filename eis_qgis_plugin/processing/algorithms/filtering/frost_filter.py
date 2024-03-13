from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISFrostFilter(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "frost_filter"
        self._display_name = "Frost filter"
        self._group = "Filtering"
        self._group_id = "filtering"
        self._short_help_string = '''
            Apply a Frost filter to the input raster.
            Higher number of looks result in better edge preservation.
            '''

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "size",
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

        damping_factor = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Damping factor",
            minValue=0,
            defaultValue=1.0,
            type=QgsProcessingParameterNumber.Double,
        )
        damping_factor.setHelp(
            '''
            Extent of exponential damping effect on filtering.
            Larger damping values preserve edges better but smooths less.
            Smaller values produce more smoothing.
            '''
        )
        self.addParameter(damping_factor)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Output raster"
        )
        output_raster_param.setHelp("The output raster data set.")
        self.addParameter(output_raster_param)
