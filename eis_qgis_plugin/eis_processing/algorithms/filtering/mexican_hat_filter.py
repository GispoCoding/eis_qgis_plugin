from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISMexicanHatFilter(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "mexican_hat_filter"
        self._display_name = "Mexican hat filter"
        self._group = "Filtering"
        self._group_id = "filtering"
        self._short_help_string = """
        Apply a Mexican hat filter to the input raster.
        
        Support two directions of calculating the kernel values:
        Circular: Lowpass filter for smoothing.
        Rectangular: Highpass filter for edge detection. Results may need further normalization.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "sigma",
            "truncate",
            "size",
            "direction",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        input_raster_param.setHelp("The input raster data set.")
        self.addParameter(input_raster_param)

        sigma_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Sigma",
            minValue=0.001,
            defaultValue=1.0,
            type=QgsProcessingParameterNumber.Double,
        )
        sigma_param.setHelp("The standard deviation.")
        self.addParameter(sigma_param)

        truncate_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Truncate",
            minValue=0.001,
            defaultValue=4.0,
            type=QgsProcessingParameterNumber.Double,
        )
        truncate_param.setHelp(
            '''
            The truncation factor for the gaussian kernel based on the sigma value.
            Only if size is not given.
            E.g., for sigma = 1 and truncate = 4.0, the kernel size is 9x9.
            '''
        )
        self.addParameter(truncate_param)

        size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            description="Size",
            optional=True,
        )
        size_param.setHelp(
            '''
            The size of the filter window. E.g., 3 means a 3x3 window.
            '''
        )
        self.addParameter(size_param)
           
        direction_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[4],
            description="Shape",
            options=["circular", "rectangular"],
            defaultValue="circular",
        )
        direction_param.setHelp(
            '''
            The direction of calculating the kernel values.
            Can be either 'rectangular' or 'circular'.
            '''
        )
        self.addParameter(direction_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[5], description="Mexican hat filter output"
        )
        output_raster_param.setHelp("The output raster data set.")
        self.addParameter(output_raster_param)
