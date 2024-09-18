from qgis.core import (
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISSplitRasterBands(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "split_raster_bands"
        self._display_name = "Split raster bands"
        self._group = "Utilities"
        self._group_id = "utilities"
        self._short_help_string = """
            Splits multiband raster into singleband rasters.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "output_dir"]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0],
            description="Input raster",
        )
        input_raster_param.setHelp("Input multiband raster to be split.")
        self.addParameter(input_raster_param)

        output_folder_param = QgsProcessingParameterFolderDestination(
            name=self.alg_parameters[1],
            description="Output folder"
        )
        output_folder_param.setHelp("Output folder where the singleband rasters will be saved.")
        self.addParameter(output_folder_param)
