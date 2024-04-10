from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISDbscanVector(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "dbscan_vector"
        self._display_name = "DBSCAN (vector)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
        Perform DBSCAN clustering on a Geodataframe.

        The attributes to include in clustering can be controlled with `include_coordinates` and \
        `columns` parameters. Coordinates will add spatial proximity and columns the selected \
        attributes in the cluster creation process. If coordinates are omitted, at least some columns \
        need to be included.

        If columns are included and the attributes have different scales and represent different \
        phenomena, consider normalizing or standardizing data before running DBSCAN to avoid biased clusters.

        Note that the results depend heavily on the parameter values that might require careful tuning. \
        Note also that clustering can be computationally intesive for large datasets, for highly dimensional data \
        consider dimensionality reduction techniques such as PCA.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_vector",
            "include_coordinates",
            "columns",
            "max_distance",
            "min_samples",
            "output_vector",
        ]

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector file with features to be clustered.")
        self.addParameter(input_vector_param)

        include_coordinates_param = QgsProcessingParameterBoolean(
            name=self.alg_parameters[1],
            description="Include coordinates",
            defaultValue=True
        )
        include_coordinates_param.setHelp(
            "If feature coordinates (spatial proximity) will be included in the clustering process."
        )
        self.addParameter(include_coordinates_param)

        columns_param = QgsProcessingParameterField(
            self.alg_parameters[2],
            description="Columns",
            parentLayerParameterName=self.alg_parameters[0],
            allowMultiple=True,
            optional=True
        )
        columns_param.setHelp(
            "Columns/attributes in the input vector to be included in the clustering process."
        )
        self.addParameter(columns_param)

        max_distance_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            description="Maximum distance",
            minValue=0.0,
            defaultValue=0.5,
            type=QgsProcessingParameterNumber.Double,
        )
        max_distance_param.setHelp(
            "The maximum distance between two samples for one to be considered as in the neighborhood of the other.")
        self.addParameter(max_distance_param)

        min_samples_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4], description="Minimum number of samples", minValue=2, defaultValue=5
        )
        min_samples_param.setHelp(
            "The number of samples in a neighborhood for a point to be considered as a core point."
        )
        self.addParameter(min_samples_param)

        output_vector_param = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[5], description="Output vector"
        )
        output_vector_param.setHelp("Output vector file with new cluster label column.")
        self.addParameter(output_vector_param)
