from qgis.core import (
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISZScoreNormalization(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "z_score_normalization"
        self._display_name = "Z score normalization"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = """
            Normalize data based on mean and standard deviation.

            Results will have a mean = 0 and standard deviation = 1. \
            This transformation is also known as standardization.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "output_raster"]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("Input raster to be transformed.")
        self.addParameter(input_raster_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[1], description="Output raster"
        )
        output_raster_param.setHelp("Output raster with the transformed data.")
        self.addParameter(output_raster_param)
