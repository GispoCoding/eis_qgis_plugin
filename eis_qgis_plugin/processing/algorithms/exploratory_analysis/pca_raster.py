from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterEnum,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPcaRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "compute_pca_raster"
        self._display_name = "PCA (raster)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
            Compute PCA for raster data.

            Before computation, data is automatically standardized, and nodata values removed \
            or replaced with band means.

            All bands from input rasters are read and stacked. Number of components should be at least the total \
            number of bands.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_rasters", "number_of_components", "nodata_handling", "output_raster"]

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                name=self.alg_parameters[0], description="Input rasters", layerType=QgsProcessing.TypeRaster
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1],
                description="Number of components",
                defaultValue=3,
                minValue=2
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[2],
                description="Nodata handling",
                options=["remove", "replace"],
                defaultValue="remove"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[3], description="Output raster"
            )
        )
