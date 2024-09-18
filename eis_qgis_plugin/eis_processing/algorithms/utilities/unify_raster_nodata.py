from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISUnifyRasterNodata(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "unify_raster_nodata"
        self._display_name = "Unify raster nodata"
        self._group = "Utilities"
        self._group_id = "utilities"
        self._short_help_string = """
            Unifies nodata for the input rasters.

            Sets nodata in raster metadata to the specified value and replaces all found old nodata \
            pixels with new nodata pixels for all rasters. 

            Old nodata values are read from raster metadata. If some raster metadata are incorrect, \
            fix them first with "Set raster nodata" or "Convert raster nodata" tools.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_rasters", "new_nodata", "output_dir"]

        input_raster_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[0],
            description="Input rasters",
            layerType=QgsProcessing.TypeRaster,
        )
        input_raster_param.setHelp("Input rasters with nodata to be unified.")
        self.addParameter(input_raster_param)

        new_nodata_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="New nodata",
            defaultValue=-9999,
            type=QgsProcessingParameterNumber.Double,
        )
        new_nodata_param.setHelp("New nodata value used for the rasters.")
        self.addParameter(new_nodata_param)

        output_folder_param = QgsProcessingParameterFolderDestination(
            name=self.alg_parameters[2],
            description="Output raster"
        )
        output_folder_param.setHelp("Output folder where the unified rasters will be saved.")
        self.addParameter(output_folder_param)
