from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterExtent,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISKrigingInterpolation(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "kriging_interpolation"
        self._display_name = "Kriging interpolation"
        self._group = "Vector processing"
        self._group_id = "vector_processing"
        self._short_help_string = """
        Perform kriging interpolation on vector data.

        Supports both 'ordinary' and 'universal' kriging. Available variogram models are 'linear', 'power', \
        'gaussian', 'spherical' and 'exponential'.
        
        The output raster grid can be defined either using base raster or manually setting pixel size and extent.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_vector",
            "target_column",
            "base_raster",
            "pixel_size",
            "extent",
            "variogram_model",
            "coordinates_type",
            "method",
            "output_raster",
        ]

        input_vector_param = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector file with features to be interpolated.")
        self.addParameter(input_vector_param)

        target_column_param = QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Interpolation attribute",
            parentLayerParameterName=self.alg_parameters[0],
            type=QgsProcessingParameterField.Numeric,
        )
        target_column_param.setHelp("Attribute to interpolate.")
        self.addParameter(target_column_param)

        base_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[2],
            description="Base raster",
            optional=True
        )
        base_raster_param.setHelp("Base raster to define grid properties of output raster.")
        self.addParameter(base_raster_param)

        pixel_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3], description="Pixel size", optional=True
        )
        pixel_size_param.setHelp("Pixel size of the output raster. Only used if base raster isn't defined.")
        self.addParameter(pixel_size_param)

        raster_extent_param = QgsProcessingParameterExtent(
            name=self.alg_parameters[4], description="Raster extent", optional=True
        )
        raster_extent_param.setHelp(
            "Extent of the output raster. Only used if base raster isn't defined."
        )
        self.addParameter(raster_extent_param)

        variogram_model_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[5],
            description="Variogram model",
            options=["linear", "power", "gaussian", "spherical", "exponential"],
            defaultValue="linear",
        )
        variogram_model_param.setHelp("Variogram model to be used.")
        self.addParameter(variogram_model_param)

        coordinates_type_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[6],
            description="Coordinates type",
            options=["geographic", "euclidean"],
            defaultValue="geographic",
        )
        coordinates_type_param.setHelp(
            "Determines are coordinates on a plane ('euclidean') or a sphere ('geographic'). \
            Used only in ordinary kriging."
        )
        self.addParameter(coordinates_type_param)

        kriging_method_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[7],
            description="Kriging method",
            options=["ordinary", "universal"],
            defaultValue="ordinary",
        )
        kriging_method_param.setHelp("Kriging method to use.")
        self.addParameter(kriging_method_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[8],
            description="Kriging output",
        )
        output_raster_param.setHelp("Output interpolation raster.")
        self.addParameter(output_raster_param)
