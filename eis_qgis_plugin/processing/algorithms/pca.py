from qgis.core import (
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPca(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "pca"
        self._display_name = "Principal component analysis"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Compute PCA"

    def initAlgorithm(self, config=None):

        self.alg_parameters = ["input_raster", "components", "output_folder"]

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
            QgsProcessingParameterFolderDestination(
                name=self.alg_parameters[2], description="Output folder"
            )
        )
