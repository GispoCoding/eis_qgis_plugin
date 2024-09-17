from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterEnum,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPcaRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "compute_pca_raster"
        self._display_name = "PCA (raster)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
            Compute PCA for raster data.

            All bands from input rasters are read and stacked.

            Before computation, data is automatically standardized, and nodata values removed \
            or replaced with band means.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_rasters", "number_of_components", "nodata_handling", "output_raster"]

        input_rasters_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[0], description="Input rasters", layerType=QgsProcessing.TypeRaster
        )
        input_rasters_param.setHelp("Input rasters to be used for PCA.")
        self.addParameter(input_rasters_param)

        nr_of_components_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Number of components",
            defaultValue=3,
            minValue=2
        )
        nr_of_components_param.setHelp(
            "Number of principal components to compute. Number of components should be at \
            least the total number of rasters/bands.")
        self.addParameter(nr_of_components_param)

        nodata_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[2],
            description="Nodata handling",
            options=["remove", "replace"],
            defaultValue="remove"
        )
        nodata_param.setHelp(
            "If nodata should be removed for the time of PCA computation or replaced with raster band means."
        )
        self.addParameter(nodata_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Output raster"
        )
        output_raster_param.setHelp(
            "Output multiband raster where each band has data of the corresponding principal component.")
        self.addParameter(output_raster_param)
