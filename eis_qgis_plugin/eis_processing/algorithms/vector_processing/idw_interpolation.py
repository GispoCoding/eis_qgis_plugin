from qgis.core import (
    QgsProcessingParameterExtent,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISIdwInterpolation(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "idw_interpolation"
        self._display_name = "IDW interpolation"
        self._group = "Vector processing"
        self._group_id = "vector_processing"
        self._short_help_string = """
        Perform inverse distance weighting (IDW) interpolation on vector data.
        
        The output raster grid can be defined either using base raster or manually setting pixel size and extent.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_vector",
            "target_column",
            "base_raster",
            "pixel_size",
            "extent",
            "power",
            "search_radius",
            "output_raster",
        ]

        input_vector_param = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector file with features to be interpolated.")
        self.addParameter(input_vector_param)

        column_param = QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Interpolation attribute",
            parentLayerParameterName=self.alg_parameters[0],
            type=QgsProcessingParameterField.Numeric,
        )
        column_param.setHelp("Attribute to interpolate.")
        self.addParameter(column_param)

        base_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[2],
            description="Base raster",
            optional=True
        )
        base_raster_param.setHelp("Base raster to define grid properties of output raster.")
        self.addParameter(base_raster_param)

        pixel_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3], description="Pixel size", minValue=0, optional=True
        )
        pixel_size_param.setHelp("Pixel size of the output raster. Only used if base raster isn't defined.")
        self.addParameter(pixel_size_param)

        extent_param = QgsProcessingParameterExtent(
            name=self.alg_parameters[4], description="Raster extent", optional=True
        )
        extent_param.setHelp(
            "Extent of the output raster. Only used if base raster isn't defined."
        )
        self.addParameter(extent_param)

        power_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[5], description="Power", defaultValue=2
        )
        power_param.setHelp(
            "The value for determining the rate at which the weights decrease. \
            As power increases, the weights for distant points decrease rapidly.")
        self.addParameter(power_param)

        search_radius_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[6], description="Search radius", minValue=0.0, optional=True
        )
        search_radius_param.setHelp(
            "The search radius within which to consider points for interpolation. If left empty, all points are used."
            )
        self.addParameter(search_radius_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[7], description="IDW output"
        )
        output_raster_param.setHelp("Output interpolation raster.")
        self.addParameter(output_raster_param)
