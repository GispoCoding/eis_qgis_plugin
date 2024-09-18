from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISBinarize(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "binarize"
        self._display_name = "Binarize"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = """
            Binarize data based on a given threshold.

            Replaces values less or equal threshold with 0. \
            Replaces values greater than the threshold with 1.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "threshold", "output_raster"]
        
        input_vector_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_vector_param.setHelp("Input raster to be binarized.")
        self.addParameter(input_vector_param)

        binarizing_threshold_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Binarizing threshold",
            type=QgsProcessingParameterNumber.Double,
        )
        binarizing_threshold_param.setHelp("Threshold value for binarization.")
        self.addParameter(binarizing_threshold_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[2],
            description="Output raster",
        )
        output_raster_param.setHelp("Output raster with transformed data.")
        self.addParameter(output_raster_param)
