from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISAgterbergChengCiTest(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "agterberg_cheng_ci_test"
        self._display_name = "Agterberg-Cheng CI test (weights of evidence)"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = "Perform the conditional independence test presented by Agterberg-Cheng (2002)."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_posterior_probabilities",
            "input_posterior_probabilities_std",
            "input_weights_table",
            "save_summary"
        ]

        posterior_probabilities_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Posterior probabilities"
        )
        posterior_probabilities_param.setHelp("Raster of posterior probabilites.")
        self.addParameter(posterior_probabilities_param)

        posterior_probabilities_std_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[1], description="Standard deviations"
        )
        posterior_probabilities_std_param.setHelp(
            "Raster of standard deviations in the posterior probability calculations."
        )
        self.addParameter(posterior_probabilities_std_param)

        input_weights_file = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[2], description="Results table", types=[QgsProcessing.SourceType.TypeVector]
        )
        input_weights_file.setHelp(
            "CSV output of calculate weights algorithm. Needs to include columns 'Deposit count' and 'Pixel count'."
        )
        self.addParameter(input_weights_file)

        save_summary_param = QgsProcessingParameterFileDestination(
            name=self.alg_parameters[3], description="Save summary", optional=True
        )
        save_summary_param.setHelp("File path for saving the test results (summary) in a text file.")
        self.addParameter(save_summary_param)
