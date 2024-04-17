from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISSetRasterNodata(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "set_raster_nodata"
        self._display_name = "Set raster nodata"
        self._group = "Utilities"
        self._group_id = "utilities"
        self._short_help_string = """
            Sets nodata value in raster metadata to the specified value.

            Does NOT convert any pixel values, only changes raster metadata. This tool is inteded \
            to fix incorrect raster metadata.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "new_nodata", "output_raster"]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0],
            description="Input raster",
        )
        input_raster_param.setHelp("Input raster with nodata to be set.")
        self.addParameter(input_raster_param)

        new_nodata_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="New nodata",
            defaultValue=-9999,
            type=QgsProcessingParameterNumber.Double,
        )
        new_nodata_param.setHelp("New nodata value.")
        self.addParameter(new_nodata_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[2],
            description="Output raster"
        )
        output_raster_param.setHelp("Output raster with nodata value in its metadata.")
        self.addParameter(output_raster_param)
