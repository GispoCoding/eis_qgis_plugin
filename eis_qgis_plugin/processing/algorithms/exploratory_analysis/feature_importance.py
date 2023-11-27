from qgis.core import (
    QgsProcessingParameterFile,
    QgsProcessingParameterEnum,
    QgsProcessingParameterString,
    QgsProcessingParameterNumber,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


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
            "base_estimator",
            "test_x",
            "test_y",
            "feature_column",
            "number_of_repetitions",
            "random_state"
            ]

        # TODO! Need to figure out how to add set_params(dict)
        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[0],
                description="Base Estimator",
                options=["get_metadata_routing()", "get_params(deep=True)"],
                defaultValue="get_metadata_routing()",
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                name=self.alg_parameters[1],
                description="Testing feature data (X)",
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                name=self.alg_parameters[2],
                description="Testing feature data (Y)"
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                name=self.alg_parameters[2],
                description="Feature columns",
                multiLine=True
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[3],
                description="Number of repetitions",
                defaultValue=50
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[4],
                description="Random state",
                defaultValue=0
            )
        )
