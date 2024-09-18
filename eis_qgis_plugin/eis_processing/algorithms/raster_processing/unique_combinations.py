from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISUniqueCombinations(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "unique_combinations"
        self._display_name = "Unique combinations"
        self._group = "Unique Combinations"
        self._group_id = "raster_processing"
        self._short_help_string = """
            Generate combinations of values between rasters.

            All bands from all rasters are used to generate the combinations.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "output_raster"
        ]

        input_rasters_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[0],
            description="Input rasters",
            layerType=QgsProcessing.TypeRaster,
        )
        input_rasters_param.setHelp("Input rasters used to generate the unique combinations.")
        self.addParameter(input_rasters_param)

        output_raster = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[1],
            description="Output raster"
        )
        output_raster.setHelp("The output combination raster.")
        self.addParameter(output_raster)
