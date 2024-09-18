from qgis.core import QgsProcessingParameterRasterLayer

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISSummarizeProbabilityMetrics(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "summarize_probability_metrics"
        self._display_name = "Summarize probability metrics"
        self._group = "Evaluation"
        self._group_id = "evaluation"
        self._short_help_string = """
        Generate a comprehensive report of various evaluation metrics for classification probabilities.

        The output includes ROC AUC, log loss, average precision and Brier score loss.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["true_labels", "probabilities"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0],
                description="True labels",
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[1], description="Probabilities"
            )
        )
