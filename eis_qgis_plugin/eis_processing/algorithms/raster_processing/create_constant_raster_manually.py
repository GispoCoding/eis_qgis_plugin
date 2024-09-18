from qgis.core import (
    QgsProcessingParameterCrs,
    QgsProcessingParameterExtent,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISCreateConstantRasterManually(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "create_constant_raster_manually"
        self._display_name = "Create constant raster manually"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = """
        Create a constant raster manually by defining CRS, extent and pixel size.
        
        If the resulting raster height and width are not exact multiples of the pixel size, the \
        output raster extent will differ slightly from the defined extent.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "constant_value",
            "target_epsg",
            "extent",
            "target_pixel_size",
            "nodata_value",
            "output_raster",
        ]

        constant_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[0],
            description="Constant value",
            type=QgsProcessingParameterNumber.Double,
        )
        constant_value_param.setHelp("The constant value of the output raster.")
        self.addParameter(constant_value_param)

        target_epsg_param = QgsProcessingParameterCrs(
            name=self.alg_parameters[1],
            description="Target CRS",
        )
        target_epsg_param.setHelp("The CRS of the output raster.")
        self.addParameter(target_epsg_param)

        extent_param = QgsProcessingParameterExtent(
            name=self.alg_parameters[2],
            description="Extent",
        )
        extent_param.setHelp("The extent of the output raster.")
        self.addParameter(extent_param)

        target_pixel_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            description="Target pixel size",
        )
        target_pixel_size_param.setHelp("The pixel size of the output raster.")
        self.addParameter(target_pixel_size_param)

        nodata_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4],
            description="Nodata value",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=-9999
        )
        nodata_value_param.setHelp("The nodata value of the output raster.")
        self.addParameter(nodata_value_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[5], description="Output raster"
        )
        output_raster_param.setHelp("The output constant raster.")
        self.addParameter(output_raster_param)
