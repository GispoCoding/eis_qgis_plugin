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

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm
from eis_qgis_plugin.utils.misc_utils import parse_string_list_parameter_and_run_command


class EISReclassifyWithManualBreaks(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "reclassify_with_manual_breaks"
        self._display_name = "Reclassify with manual breaks"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = """
        Reclassify raster with manual breaks.
        
        If bands are not given, all bands are used for classification.
        """

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
            name=self.alg_parameters[3], description="Reclassified raster (manual breaks)"
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

        results = parse_string_list_parameter_and_run_command(
            self,
            1,
            parameters,
            context,
            feedback
        )

        return results
