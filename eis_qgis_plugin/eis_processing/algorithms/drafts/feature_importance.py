from qgis.core import (
    QgsProcessingParameterFile,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterString,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISFeatureImportance(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "feature_importance"
        self._display_name = "Evaluate feature importance"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Feature importance"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "classifier_or_model",
            "test_x",
            "test_y",
            "feature_columns",
            "number_of_repetitions",
            "random_state"
            ]

        self.addParameter(
            QgsProcessingParameterFile(
                name=self.alg_parameters[0],
                description="Classifier/Model",
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[1],
                description="Testing feature data (X)",
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[2],
                description="Testing feature data (Y)"
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                name=self.alg_parameters[3],
                description="Feature columns",
                multiLine=True
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[4],
                description="Number of repetitions",
                defaultValue=50
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[5],
                description="Random state",
                defaultValue=0
            )
        )
