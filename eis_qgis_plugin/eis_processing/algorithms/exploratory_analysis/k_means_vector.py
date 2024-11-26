from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISKMeansVector(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "k_means_clustering_vector"
        self._display_name = "K-means clustering (vector)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
        Perform k-means clustering on vector data.

        The attributes to include in clustering can be controlled with `include_coordinates` and \
        `columns` parameters. Coordinates will add spatial proximity and columns the selected \
        attributes in the cluster creation process. If coordinates are omitted, at least some columns \
        need to be included.

        If columns are included and the attributes have different scales and represent different \
        phenomena, consider normalizing or standardizing data before running k-means to avoid biased clusters.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_vector",
            "include_coordinates",
            "columns",
            "number_of_clusters",
            "random_state",
            "output_vector",
        ]

        input_vector_param = QgsProcessingParameterVectorLayer(
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
            type=QgsProcessingParameterField.Numeric,
            allowMultiple=True,
            optional=True
        )
        columns_param.setHelp(
            "Columns/attributes in the input vector to be included in the clustering process."
        )
        self.addParameter(columns_param)

        nr_of_clusters_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            description="Number of clusters",
            minValue=1,
            optional=True,
        )
        nr_of_clusters_param.setHelp(
            "The number of clusters to form. If not provided, optimal number " +
            "of clusters is computed using the elbow method.")
        self.addParameter(nr_of_clusters_param)

        random_state_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4], description="Random state", optional=True
        )
        random_state_param.setHelp(
            "A random number seed for centroid initialization to make the randomness deterministic."
        )
        self.addParameter(random_state_param)

        output_vector_param = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[5], description="Output vector"
        )
        output_vector_param.setHelp("Output vector file with new cluster label column.")
        self.addParameter(output_vector_param)
