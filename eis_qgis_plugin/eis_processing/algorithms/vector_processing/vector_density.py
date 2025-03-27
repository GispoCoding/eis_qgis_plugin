from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterExtent,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISVectorDensity(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "vector_density"
        self._display_name = "Vector density"
        self._group = "Vector processing"
        self._group_id = "vector_processing"
        self._short_help_string = "Compute density of geometries within raster"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_vector",
            "base_raster",
            "pixel_size",
            "extent",
            "buffer_value",
            "statistic",
            "output_raster",
        ]

        input_vector_param = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector with geometries to compute density for.")
        self.addParameter(input_vector_param)

        base_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[1], description="Base raster", optional=True
        )
        base_raster_param.setHelp("Base raster to define grid properties of output raster.")
        self.addParameter(base_raster_param)

        pixel_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2], description="Pixel size", optional=True
        )
        pixel_size_param.setHelp("Pixel size of the output raster. Only used if base raster isn't defined.")
        self.addParameter(pixel_size_param)

        extent_param = QgsProcessingParameterExtent(
            name=self.alg_parameters[3], description="Extent", optional=True
        )
        extent_param.setHelp(
            "Extent of the output raster. Only used if base raster isn't defined."
        )
        self.addParameter(extent_param)

        buffer_param =QgsProcessingParameterNumber(
            name=self.alg_parameters[4], description="Buffer", optional=True
        )
        buffer_param.setHelp("Size of buffer added around geometries before computing density.")
        self.addParameter(buffer_param)

        statistic_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[5],
            description="Statistic",
            options=["density", "count"],
            defaultValue="density",
        )
        statistic_param.setHelp("Statistic to be used in density computation.")
        self.addParameter(statistic_param)            

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[6],
            description="Vector density output",
        )
        output_raster_param.setHelp("Output density raster.")
        self.addParameter(output_raster_param)
