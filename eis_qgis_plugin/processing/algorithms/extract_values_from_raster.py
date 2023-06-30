from qgis.core import (
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterFileDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm

class EISExtractValuesFromRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "extract_values_from_raster"
        self._display_name = "Extract values from raster"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Extract values from raster"

    def initAlgorithm(self, config=None):
        
        self.alg_parameters = ["raster_list", "raster_values", "column_names", "output_dataframe"]

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                name=self.alg_parameters[0], description="Raster values"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[1], description="Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                name=self.alg_parameters[2], description="Raster column names"
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[3], description="Output dataframe"
            )
        )
