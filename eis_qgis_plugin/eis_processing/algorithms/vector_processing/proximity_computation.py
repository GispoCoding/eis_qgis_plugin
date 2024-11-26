from qgis.core import (
    QgsProcessingParameterExtent,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISProximityComputation(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "proximity_computation"
        self._display_name = "Proximity computation"
        self._group = "Vector processing"
        self._group_id = "vector_processing"
        self._short_help_string = """
        Compute proximities from raster cells to nearest vector geometries.

        Scales output raster values linearly based on given `max_distance_value` and `geometries_value`.
        
        The output raster grid can be defined either using base raster or manually setting pixel size and extent.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_vector",
            "base_raster",
            "pixel_size",
            "extent",
            "max_distance",
            "max_distance_value",
            "geometries_value",
            "output_raster"
        ]

        input_vector_param = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector with geometries to determine proximity to.")
        self.addParameter(input_vector_param)

        base_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[1], description="Base raster", optional=True
        )
        base_raster_param.setHelp("Base raster to define grid properties of output raster.")
        self.addParameter(base_raster_param)

        pixel_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2], description="Pixel size", minValue=0, optional=True
        )
        pixel_size_param.setHelp("Pixel size of the output raster. Only used if base raster isn't defined.")
        self.addParameter(pixel_size_param)

        extent_param = QgsProcessingParameterExtent(
            name=self.alg_parameters[3], description="Raster extent", optional=True
        )
        extent_param.setHelp(
            "Extent of the output raster. Only used if base raster isn't defined."
        )
        self.addParameter(extent_param)

        max_distance_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4],
            description="Max distance",
            type=QgsProcessingParameterNumber.Double,
            minValue=0.0
        )
        max_distance_param.setHelp("Maximum distance in the output raster.")
        self.addParameter(max_distance_param)

        max_distance_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[5],
            description="Max distance value",
            type=QgsProcessingParameterNumber.Double,
            minValue=0.0
        )
        max_distance_value_param.setHelp(
            "Value at and beyond given max distance. Used for scaling the output raster values."
        )
        self.addParameter(max_distance_value_param)

        geometries_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[6],
            description="Geometries value",
            type=QgsProcessingParameterNumber.Double,
            minValue=1.0
        )
        geometries_value_param.setHelp("Value at geometries. Used for scaling the output raster values.")
        self.addParameter(geometries_value_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[7], description="Output raster"
        )
        output_raster_param.setHelp("Output raster with proximities to closest geometries.")
        self.addParameter(output_raster_param)
