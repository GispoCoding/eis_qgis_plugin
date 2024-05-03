from qgis.core import QgsProcessingParameterEnum, QgsProcessingParameterRasterLayer

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISScorePredictions(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "score_predictions"
        self._display_name = "Score predictions"
        self._group = "Evaluation"
        self._group_id = "evaluation"
        self._short_help_string = """
        Score model predictions with given metrics.

        One or multiple metrics can be defined for scoring.

        Supported classifier metrics: "accuracy", "precision", "recall", "f1". \
        Supported regressor metrics: "mse", "rmse", "mae", "r2".
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["true_labels", "predictions", "metrics"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0],
                description="True labels",
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[1], description="Predictions"
            )
        )
        
        metrics_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[2],
            description="Metrics",
            options=["accuracy", "precision", "recall", "f1", "auc", "mse", "rmse", "mae", "r2"],
            allowMultiple=True
        )
        metrics_param.setHelp(
            "Metrics calculated. The selected metrics need to be applicable for model type (classifier or regressor)."
        )
        self.addParameter(metrics_param)