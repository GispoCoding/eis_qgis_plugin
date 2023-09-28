from qgis.core import (
    QgsProcessingParameterRasterLayer
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISDescriptiveStatisticsRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "descriptive_statistics_raster"
        self._display_name = "Descriptive statistics (raster)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Generate descriptive statistics for a raster layer"

    def initAlgorithm(self, config=None):

        # self.alg_parameters = ["input_file", "output_file"]
        self.alg_parameters = ["input_file"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input layer"
            )
        )

        # self.addParameter(
        #     QgsProcessingParameterFileDestination(
        #         name=self.alg_parameters[1],
        #         description="Output file",
        #     )
        # )
