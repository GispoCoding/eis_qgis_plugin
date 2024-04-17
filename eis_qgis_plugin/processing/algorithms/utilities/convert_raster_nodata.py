from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISConvertRasterNodata(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "convert_raster_nodata"
        self._display_name = "Convert raster nodata"
        self._group = "Utilities"
        self._group_id = "utilities"
        self._short_help_string = """
            Convert old nodata value to a new nodata value.

            Sets nodata in raster metadata to the specified value and replaces all found old nodata \
            pixels with new nodata pixels.

            Old nodata value can be specified as a parameter, but is not needed when raster metadata \
            has the correct nodata value.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "old_nodata", "new_nodata", "output_raster"]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0],
            description="Input raster",
        )
        input_raster_param.setHelp("Input raster with nodata to be converted.")
        self.addParameter(input_raster_param)

        old_nodata_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Old nodata",
            type=QgsProcessingParameterNumber.Double,
            optional=True
        )
        old_nodata_param.setHelp(
            "Existing value that represents nodata in the input raster. If raster metadata is correct this \
                does not need to be set."
            )
        self.addParameter(old_nodata_param)

        new_nodata_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="New nodata",
            defaultValue=-9999,
            type=QgsProcessingParameterNumber.Double,
        )
        new_nodata_param.setHelp("New nodata value used in the output raster.")
        self.addParameter(new_nodata_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3],
            description="Output raster"
        )
        output_raster_param.setHelp("Output raster with nodata values converted.")
        self.addParameter(output_raster_param)
