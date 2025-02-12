from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISLogTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "log_transform"
        self._display_name = "Logarithmic transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = """
        Perform a logarithmic transformation on the provided data.
        
        The supported logarithm types are 'log2', 'log10', and 'ln'.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "log_type", "output_raster"]

        input_raster_param =  QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("Input raster to be transformed.")
        self.addParameter(input_raster_param)

        log_type_param =  QgsProcessingParameterEnum(
            name=self.alg_parameters[1],
            description="Log type",
            options=["log2", "log10", "ln"],
        )
        log_type_param.setHelp("The base for logarithmic transformation.")
        self.addParameter(log_type_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[2], description="Log transformed raster"
        )
        output_raster_param.setHelp("Output raster with transformed data.")
        self.addParameter(output_raster_param)
