import re
from typing import Any, Dict, Optional

from qgis.core import (
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingParameterBand,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterString,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm
from eis_qgis_plugin.processing.eis_toolkit_invoker import EISToolkitInvoker


class EISReclassifyWithManualBreaks(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "reclassify_with_manual_breaks"
        self._display_name = "Reclassify with manual breaks"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Reclassify raster with manual breaks."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "breaks",
            "bands",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("The input raster to be reclassified.")
        self.addParameter(input_raster_param)

        breaks_param = QgsProcessingParameterString(
            name=self.alg_parameters[1],
            description="Breaks"
        )
        breaks_param.setHelp(
            '''The breaks used in reclassification. Input the breaks as a comma-separated list. 
            For example: 0, 10, 20, 30, 40, 50.'''
        )
        self.addParameter(breaks_param)

        bands_param = QgsProcessingParameterBand(
            name=self.alg_parameters[2],
            description="Raster band",
            parentLayerParameterName=self.alg_parameters[0],
        )
        bands_param.setHelp("The band to be reclassified.")
        self.addParameter(bands_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Output raster"
        )
        output_raster_param.setHelp("The output reclassified raster.")
        self.addParameter(output_raster_param)


    def processAlgorithm(
        self,
        parameters: Dict[str, QgsProcessingParameterDefinition],
        context: QgsProcessingContext,
        feedback: Optional[QgsProcessingFeedback]
    ) -> Dict[str, Any]:
        if feedback is None:
            feedback = QgsProcessingFeedback()
        
        breaks_param_i = 1
        # Handle the manual breaks
        breaks_raw = self.parameterAsString(parameters, self.alg_parameters[breaks_param_i], context).lower()
        values = re.split(';|,', breaks_raw)
        break_options = []
        for value in values:
            break_options.append("--" + self.alg_parameters[breaks_param_i].replace("_", "-"))
            break_options.append(value) 

        # Remove breaks from the list to not prepare them again in the next step
        self.alg_parameters.pop(breaks_param_i)
        typer_args, typer_options = self.prepare_arguments(parameters, context)
        typer_options += break_options  # Combine lists

        toolkit_invoker = EISToolkitInvoker()
        toolkit_invoker.assemble_cli_command(self.name(), typer_args, typer_options)
        results = toolkit_invoker.run_toolkit_command(feedback)

        self.get_results(results, parameters)

        return results
