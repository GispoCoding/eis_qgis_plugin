from qgis.core import QgsProcessingParameterRasterLayer

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISSummarizeLabelMetricsBinary(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "summarize_label_metrics_binary"
        self._display_name = "Summarize label metrics binary"
        self._group = "Evaluation"
        self._group_id = "evaluation"
        self._short_help_string = """
        Generate a comprehensive report of various evaluation metrics for binary classification results.

        The output includes accuracy, precision, recall, F1 scores and confusion matrix elements \
        (true negatives, false positives, false negatives, true positives).
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["true_labels", "predictions"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0],
                description="True labels",
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[1], description="Predicted labels"
            )
        )
