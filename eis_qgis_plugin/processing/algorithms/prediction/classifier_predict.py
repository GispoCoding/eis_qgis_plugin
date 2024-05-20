from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFile,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISClassifierPredict(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "classifier_predict"
        self._display_name = "Classifier predict"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = """
            Predict mineral prospectivity with a trained machine learning classifier model.

            The output probability array is thresholded with the classification threshold to get predicted labels \
            raster for binary classification tasks. For multiclass classification, this parameter is not used \
            and the output classification raster has classes with highest probability for each pixel. The probability \
            raster can be thresholded afterwards with other thresholds using for example QGIS Raster Calculator.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "model_file",
            "classification_threshold",
            "output_raster_probability",
            "output_raster_classified"
        ]

        evidence_data_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[0], description="Evidence data", layerType=QgsProcessing.TypeRaster
        )
        evidence_data_param.setHelp(
            "Evidence data used for predicting. Evidence layers should match the layers used in training."
        )
        self.addParameter(evidence_data_param)

        model_file_param = QgsProcessingParameterFile(
            name=self.alg_parameters[1], description="Model file", fileFilter='.joblib (*.joblib)'
        )
        model_file_param.setHelp("The model file.")
        self.addParameter(model_file_param)

        classification_threshold_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Classification threshold",
            type=QgsProcessingParameterNumber.Double,
            minValue=0.0,
            maxValue=1.0,
            defaultValue=0.5
        )
        classification_threshold_param.setHelp("Threshold to classify label probabilities with.")
        self.addParameter(classification_threshold_param)
        
        output_raster_probability_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3],
            description="Output probability raster",
        )
        output_raster_probability_param.setHelp("Output raster with label probabilities.")
        self.addParameter(output_raster_probability_param)

        output_raster_classified_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[4],
            description="Output classified raster",
        )
        output_raster_classified_param.setHelp("Output raster with predicted labels.")
        self.addParameter(output_raster_classified_param)
