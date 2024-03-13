from qgis.core import QgsProcessingParameterBand, QgsProcessingParameterRasterLayer

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISNormalityTestRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "normality_test_raster"
        self._display_name = "Normality test (raster)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
        Compute Shapiro-Wilk normality test on input raster data.

        Normality is calculated for each selected band.
        Raster nodata values are automatically ignored.

        Displays Shapiro-Wilk statistics and p-values as a result.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "bands"]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_raster_param.setHelp("Input raster containing band data to be tested.")
        self.addParameter(input_raster_param)

        bands_param = QgsProcessingParameterBand(
            name=self.alg_parameters[1],
            parentLayerParameterName=self.alg_parameters[0],
            allowMultiple=True,
            defaultValue=[1]
        )
        bands_param.setHelp(
            "Raster band selection. If no bands are selected, normality is tested for all found bands."
        )
        self.addParameter(bands_param)
