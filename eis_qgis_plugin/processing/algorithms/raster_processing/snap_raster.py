from qgis.core import (
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISSnapRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "snap_raster"
        self._display_name = "Snap raster"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = """
            Snap a raster to same alignment with given base raster.

            Raster is snapped from its left-bottom corner to nearest snap raster grid corner in left-bottom direction.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "snap_raster", "output_raster"]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("Input raster to be snapped.")
        self.addParameter(input_raster_param)

        base_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[1], description="Base raster for snapping"
        )
        base_raster_param.setHelp("Base raster with the target grid for snapping.")
        self.addParameter(base_raster_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[2], description="Output raster"
        )
        output_raster_param.setHelp("The output snapped raster.")
        self.addParameter(output_raster_param)
