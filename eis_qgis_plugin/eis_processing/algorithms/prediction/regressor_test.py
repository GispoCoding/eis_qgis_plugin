from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFile,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISRegressorTest(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "regressor_test"
        self._display_name = "Regressor test"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = "Test trained machine learning classifier model by predicting and scoring."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "target_labels",
            "model_file",
            "test_metrics",
            "output_raster"
        ]

        evidence_data_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[0], description="Evidence data", layerType=QgsProcessing.TypeRaster
        )
        evidence_data_param.setHelp(
            "Evidence data used for predicting. Evidence layers should match the layers used in training."
        )
        self.addParameter(evidence_data_param)

        target_labels = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[1], description="Target labels"
        )
        target_labels.setHelp("Target labels to test the predictions against.")
        self.addParameter(target_labels)

        model_file_param = QgsProcessingParameterFile(
            name=self.alg_parameters[2], description="Model file", fileFilter='.joblib (*.joblib)'
        )
        model_file_param.setHelp("The model file.")
        self.addParameter(model_file_param)

        test_metrics_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[3],
            description="Test metric",
            options=["mse", "rmse", "mae", "r2"],
            defaultValue=0,
            allowMultiple=True
        )
        test_metrics_param.setHelp("Metrics calculated for the predictions.")
        self.addParameter(test_metrics_param)
        
        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[4],
            description="Regression output (test)",
        )
        output_raster_param.setHelp("Output raster with predictions.")
        self.addParameter(output_raster_param)
