from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISGaussianFilter(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "gaussian_filter"
        self._display_name = "Gaussian filter"
        self._group = "Filtering"
        self._group_id = "filtering"
        self._short_help_string = "Apply a basic gaussian filter to the input raster"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "sigma",
            "truncate",
            "size",
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
            minValue=1.0,
            defaultValue=1.0,
            type=QgsProcessingParameterNumber.Double,
        )
        sigma_param.setHelp("The standard deviation of the gaussian kernel.")
        self.addParameter(sigma_param)

        truncate_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Truncate",
            minValue=1.0,
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

        window_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            description="Size",
            optional=True,
        )
        window_size_param.setHelp(
            '''
            The size of the filter window. E.g., 3 means a 3x3 window.
            If size is not None, it overrides the dynamic size calculation based on sigma and truncate.
            '''
        )
        self.addParameter(window_size_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[4], description="Output raster"
        )
        output_raster_param.setHelp("The output raster data set.")
        self.addParameter(output_raster_param)
