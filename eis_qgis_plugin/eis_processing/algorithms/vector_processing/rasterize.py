from qgis.core import (
    # Qgis,
    QgsProcessingParameterEnum,
    QgsProcessingParameterExtent,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISRasterize(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "rasterize"
        self._display_name = "Rasterize"
        self._group = "Vector Processing"
        self._group_id = "vector_processing"
        self._short_help_string = "Rasterize a vector layer"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_vector",
            "value_column",
            "base_raster",
            "pixel_size",
            "extent",
            "default_value",
            "fill_value",
            "buffer_value",
            "merge_strategy",
            "output_raster",
        ]

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector to rasterize.")
        self.addParameter(input_vector_param)

        value_column_param = QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Value column",
            optional=True,
            parentLayerParameterName=self.alg_parameters[0],
        )
        # value_column_param.setDataType(Qgis.ProcessingFieldParameterDataType.Numeric)
        value_column_param.setHelp(
            "Column to be used when burning values. If not given, default value is used for all geometries.")
        self.addParameter(value_column_param)

        base_raster_param =  QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[2],
            description="Base raster",
            optional=True,
        )
        base_raster_param.setHelp("Base raster to define grid properties of output raster.")
        self.addParameter(base_raster_param)

        pixel_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3], description="Pixel size", optional=True
        )
        pixel_size_param.setHelp("Pixel size of the output raster. Only used if base raster isn't defined.")
        self.addParameter(pixel_size_param)

        extent_param = QgsProcessingParameterExtent(
            name=self.alg_parameters[4], description="Extent", optional=True
        )
        extent_param.setHelp(
            "Extent of the output raster. Only used if base raster isn't defined."
        )
        self.addParameter(extent_param)

        default_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[5],
            description="Default value",
            defaultValue=1.0,
        )
        default_value_param.setHelp("Default value burned into raster cells based on geometries.")
        self.addParameter(default_value_param)

        fill_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[6], description="Fill value", defaultValue=0.0
        )
        fill_value_param.setHelp("Value used outside the burned/rasterized geometry cells.")
        self.addParameter(fill_value_param)

        buffer_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[7], description="Buffer value", optional=True
        )
        buffer_param.setHelp("Size of buffer added around geometries before computing density.")
        self.addParameter(buffer_param)

        merge_strategy_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[8],
            description="Merge strategy",
            options=["replace", "add"],
            defaultValue="replace",
        )
        merge_strategy_param.setHelp(
            "How to handle overlapping geometries. \
            'add' causes overlapping geometries to add together the \
            values while 'replace' does not. Adding them together is the \
            basis for density computations where the density can be \
            calculated by using a default value of 1.0 and the sum in \
            each cell is the count of intersecting geometries."
        )
        self.addParameter(merge_strategy_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[9], description="Output raster"
        )
        output_raster_param.setHelp("Output raster.")
        self.addParameter(output_raster_param)
