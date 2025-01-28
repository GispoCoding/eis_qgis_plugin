from qgis.core import QgsProcessingParameterRasterDestination, QgsProcessingParameterRasterLayer

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISMaskRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "mask_raster"
        self._display_name = "Mask raster"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = """
        Mask input raster using the nodata locations from base raster.

        Only the first band of base raster is used to scan for nodata cells. Masking is performed to all \
        bands of input raster.

        If input rasters have mismatching grid properties, unifies rasters before masking (uses `nearest` \
        resampling, unify separately first if you need control over the resampling method).
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "base_raster", "output_raster"]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("Input raster to be masked.")
        self.addParameter(input_raster_param)

        base_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[1], description="Base raster",
        )
        base_raster_param.setHelp("The base raster used to determine nodata locations.")
        self.addParameter(base_raster_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[2], description="Masked raster"
        )
        output_raster_param.setHelp("The masked output raster.")
        self.addParameter(output_raster_param)
