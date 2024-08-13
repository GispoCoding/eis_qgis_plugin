from typing import Any, Dict, Optional

from qgis.core import (
    QgsProcessing,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterEnum,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm
from eis_qgis_plugin.processing.eis_toolkit_invoker import EISToolkitInvoker


class EISFuzzyOverlay(EISProcessingAlgorithm):

    # The map is used to get correct algorithm name for CLI (that has functions separately for each overlay)
    # from the overlay method parameter here
    OVERLAY_METHOD_MAP = {
        "and": "and_overlay",
        "or": "or_overlay",
        "sum": "sum_overlay",
        "product": "product_overlay",
        "gamma": "gamma_overlay",
    }

    def __init__(self) -> None:
        super().__init__()

        self._name = "fuzzy_overlay"
        self._display_name = "Fuzzy overlay"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = "Combine fuzzy membership data with an overlay method."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_rasters", "overlay_method", "gamma", "output_raster"]

        input_rasters_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[0], description="Input rasters", layerType=QgsProcessing.TypeRaster
        )
        input_rasters_param.setHelp("Input membership rasters for fuzzy overlay.")
        self.addParameter(input_rasters_param)

        overlay_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[1],
            description="Overlay method",
            options=["And", "Or", "Sum", "Product", "Gamma"],
            defaultValue=0,
        )
        overlay_param.setHelp("Overlay method. If 'gamma', the gamma parameter will be used.")
        self.addParameter(overlay_param)

        gamma_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Gamma",
            type=QgsProcessingParameterNumber.Double,
            minValue=0.0,
            maxValue=1.0,
            defaultValue=0.5
        )
        gamma_param.setHelp(
            "Used for gamma overlay. With gamma value of 0, the result will be the same as 'product' overlay. \
            When gamma is closer to 1, the weight of the 'sum' overlay is increased."
        )
        self.addParameter(gamma_param)
    
        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3],
            description="Output raster",
        )
        output_raster_param.setHelp("Output overlay raster.")
        self.addParameter(output_raster_param)


    def processAlgorithm(
        self, 
        parameters: Dict[str, QgsProcessingParameterDefinition],
        context: QgsProcessingContext,
        feedback: Optional[QgsProcessingFeedback]
    ) -> Dict[str, Any]:

        if feedback is None:
            feedback = QgsProcessingFeedback()

        idx = self.parameterAsEnum(parameters, self.alg_parameters[1], context)
        alg_name = self.OVERLAY_METHOD_MAP[self.parameterDefinition(self.alg_parameters[1]).options()[idx].lower()]

        self.alg_parameters.pop(1)  # Remove overlay method from delivered parameters
        if alg_name != "gamma_overlay":
            self.alg_parameters.pop(1)  # Remove gamma parameter (now at index 1)
        typer_args, typer_options, output_path = self.prepare_arguments(parameters, context)

        toolkit_invoker = EISToolkitInvoker()
        toolkit_invoker.assemble_cli_command(alg_name, typer_args, typer_options)
        results = toolkit_invoker.run_toolkit_command(feedback)

        self.get_results(results, parameters)
        results["output_path"] = output_path

        feedback.setProgress(100)

        return results
