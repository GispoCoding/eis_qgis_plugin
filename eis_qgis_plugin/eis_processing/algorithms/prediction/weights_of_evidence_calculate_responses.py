from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISWeightsOfEvidenceCalculateResponses(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "weights_of_evidence_calculate_responses"
        self._display_name = "Weights of evidence calculate responses"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = "Calculate the posterior probabilities for the given generalized weight rasters."

        self.multiple_layers_as_typer_option = True

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters_weights",
            "input_rasters_standard_deviations",
            "input_weights_table",
            "output_probabilities",
            "output_probabilities_std",
            "output_confidence_array"
        ]

        input_rasters_weights_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[0], description="Weight rasters", layerType=QgsProcessing.TypeRaster
        )
        input_rasters_weights_param.setHelp(
            "Output weight rasters (W+/Generalized W+) of the weights of evidence calculate weights tool."
        )
        self.addParameter(input_rasters_weights_param)

        input_rasters_std_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[1],
            description="Weight standard deviation rasters",
            layerType=QgsProcessing.TypeRaster,
        )
        input_rasters_std_param.setHelp("""
            Output weight standard deviation rasters (S_W+/Generalized S_W+) of the weights of evidence calculate
            weights tool."""
        )
        self.addParameter(input_rasters_std_param)

        input_weights_file = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[2], description="Results table", types=[QgsProcessing.SourceType.TypeVector]
        )
        input_weights_file.setHelp(
            "CSV output of calculate weights algorithm. Needs to include columns 'Deposit count' and 'Pixel count'."
        )
        self.addParameter(input_weights_file)

        output_probabilities_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Output posterior probabilities"
        )
        self.addParameter(output_probabilities_param)

        output_probabilities_std_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[4], description="Output standard deviations"
        )
        output_probabilities_std_param.setHelp("""
            Raster of standard deviations in the posterior probability calculations."""
        )
        self.addParameter(output_probabilities_std_param)

        output_confidence_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[5], description="Output confidence raster"
        )
        output_confidence_param.setHelp("""
            Raster of confidence of the prospectivity values obtained in the posterior probability raster."""
        )
        self.addParameter(output_confidence_param)
