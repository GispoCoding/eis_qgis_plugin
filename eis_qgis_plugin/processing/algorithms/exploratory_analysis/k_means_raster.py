from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISKMeansRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "k_means_clustering_raster"
        self._display_name = "K-means clustering (raster)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
        Perform k-means clustering on raster data.

        If the raster datasets/bands have different scales and represent different phenomena, \
        consider normalizing or standardizing data before running k-means to avoid biased clusters.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "number_of_clusters",
            "random_state",
            "output_raster",
        ]

        input_rasters_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[0],
            description="Input rasters",
            layerType=QgsProcessing.TypeRaster
        )
        input_rasters_param.setHelp(
            "Input rasters for clustering. All bands from all rasters are used. Rasters need to have \
             same grid properties."
        )
        self.addParameter(input_rasters_param)

        nr_of_clusters_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Number of clusters",
            minValue=1,
            optional=True,
        )
        nr_of_clusters_param.setHelp(
            "The number of clusters to form. If not provided, optimal number " +
            "of clusters is computed using the elbow method.")
        self.addParameter(nr_of_clusters_param)

        random_state_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2], description="Random state", optional=True
        )
        random_state_param.setHelp(
            "A random number seed for centroid initialization to make the randomness deterministic."
        )
        self.addParameter(random_state_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Output raster"
        )
        output_raster_param.setHelp("Output singleband raster with cluster numbers as pixel values.")
        self.addParameter(output_raster_param)
