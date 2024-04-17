from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISCombineRasterBands(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "combine_raster_bands"
        self._display_name = "Combine raster bands"
        self._group = "Utilities"
        self._group_id = "utilities"
        self._short_help_string = """
            Combine multiple rasters into one multiband raster.

            The input rasters can be either singleband or multiband. All bands are stacked in the order they are \
            extracted from the input raster list.

            All input rasters must have matching spatial metadata (extent, pixel size, CRS).
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_rasters", "output_raster"]

        input_raster_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[0],
            description="Input rasters",
            layerType=QgsProcessing.TypeRaster,
        )
        input_raster_param.setHelp("Input rasters to be combined.")
        self.addParameter(input_raster_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[1],
            description="Output raster"
        )
        output_raster_param.setHelp("Output multiband raster that includes all bands of all input rasters.")
        self.addParameter(output_raster_param)

