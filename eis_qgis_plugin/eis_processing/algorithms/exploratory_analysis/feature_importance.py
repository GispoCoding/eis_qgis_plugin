from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFile,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISFeatureImportance(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "feature_importance"
        self._display_name = "Feature importance"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
        Evaluate the feature importance of a Sklearn classifier or regressor.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "model_file",
            "input_rasters",
            "target_labels",
            "n_repeats",
            "random_state",
        ]

        model_file_param = QgsProcessingParameterFile(
            name=self.alg_parameters[0], description="Model file", fileFilter='.joblib (*.joblib)'
        )
        model_file_param.setHelp("The model file.")
        self.addParameter(model_file_param)

        evidence_data_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[1], description="Feature data", layerType=QgsProcessing.TypeRaster
        )
        evidence_data_param.setHelp(
            "Data on which feature importance will be computed."
        )
        self.addParameter(evidence_data_param)

        target_labels = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[2], description="Target labels"
        )
        target_labels.setHelp("Target labels.")
        self.addParameter(target_labels)

        n_repeats_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            description="N repeats",
            type=QgsProcessingParameterNumber.Integer,
            optional=True,
            defaultValue=10
        )
        n_repeats_param.setHelp("Number of iterations used when calculating feature importance.")
        self.addParameter(n_repeats_param)

        random_state_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4], description="Random state", optional=True, minValue=0
        )
        random_state_param.setHelp(
            "A random number seed for repeatability of results."
        )
        self.addParameter(random_state_param)
