from qgis.core import (
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPcaRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "pca_raster"
        self._display_name = "Principal component analysis (raster)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Compute PCA (raster)"

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "components", "output_file"]

        self.addParameter(
             QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1],
                description="Number of components",
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[2], description="Output file"
            )
        )
