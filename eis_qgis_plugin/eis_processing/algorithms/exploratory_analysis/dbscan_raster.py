from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISDbscanRaster(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "dbscan_raster"
        self._display_name = "DBSCAN (raster)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
        Perform DBSCAN clustering on raster data.

        If the raster datasets/bands have different scales and represent different phenomena, \
        consider normalizing or standardizing data before running DBSCAN to avoid biased clusters.

        Note that the results depend heavily on the parameter values that might require careful tuning. \
        Note also that clustering can be computationally intesive for large datasets, for highly dimensional data \
        consider dimensionality reduction techiniques such as PCA.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "max_distance",
            "min_samples",
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

        max_distance_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Maximum distance",
            minValue=0.0,
            defaultValue=0.5,
            type=QgsProcessingParameterNumber.Double,
        )
        max_distance_param.setHelp(
            "The maximum distance between two samples for one to be considered as in the neighborhood of the other.")
        self.addParameter(max_distance_param)

        min_samples_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2], description="Minimum number of samples", minValue=2, defaultValue=5
        )
        min_samples_param.setHelp(
            "The number of samples in a neighborhood for a point to be considered as a core point."
        )
        self.addParameter(min_samples_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="DBSCAN output"
        )
        output_raster_param.setHelp("Output singleband raster with cluster numbers as pixel values.")
        self.addParameter(output_raster_param)
