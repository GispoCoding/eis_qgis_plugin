from qgis.core import (
    QgsProcessingParameterExtent,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISIdwInterpolation(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "idw_interpolation"
        self._display_name = "IDW interpolation"
        self._group = "Vector processing"
        self._group_id = "vector_processing"
        self._short_help_string = (
            "Perform inverse distance weighting (IDW) interpolation."
        )

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_vector",
            "target_column",
            "resolution",
            "extent",
            "power",
            "output_raster",
        ]

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector file with features to be interpolated.")
        self.addParameter(input_vector_param)

        column_param = QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Column",
            parentLayerParameterName=self.alg_parameters[0]
        )
        column_param.setHelp("Interpolation attribute.")
        self.addParameter(column_param)

        pixel_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2], description="Pixel size", minValue=0
        )
        pixel_size_param.setHelp("Pixel size of the output raster.")
        self.addParameter(pixel_size_param)

        extent_param = QgsProcessingParameterExtent(
            name=self.alg_parameters[3], description="Raster extent", optional=True
        )
        extent_param.setHelp(
            "Extent of the output raster. If not defined, extent is determined from input vector extent."
        )
        self.addParameter(extent_param)

        power_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4], description="Power", defaultValue=2
        )
        power_param.setHelp(
            "The value for determining the rate at which the weights decrease. \
            As power increases, the weights for distant points decrease rapidly.")
        self.addParameter(power_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[5], description="Output raster"
        )
        output_raster_param.setHelp("Output interpolation raster.")
        self.addParameter(output_raster_param)
