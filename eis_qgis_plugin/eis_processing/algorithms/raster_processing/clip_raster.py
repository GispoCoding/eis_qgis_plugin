from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISClipRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "clip_raster"
        self._display_name = "Clip raster"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Clip a raster with polygon features."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "geometries", "output_raster"]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("Input raster to be clipped.")
        self.addParameter(input_raster_param)

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[1],
            description="Input vector",
            types=[QgsProcessing.TypeVectorPolygon]
        )
        input_vector_param.setHelp(
            "Vector layer containing the geometries to do the clipping with. Should contain only polygon features."
        )
        self.addParameter(input_vector_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[2], description="Output raster"
        )
        output_raster_param.setHelp("The clipped output raster.")
        self.addParameter(output_raster_param)
