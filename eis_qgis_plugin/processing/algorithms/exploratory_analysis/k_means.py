from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISKMeans(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "k_means_clustering"
        self._display_name = "K-means clustering"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Perform K-means clustering on input vector data."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_vector",
            "number_of_clusters",
            "random_state",
            "output_vector",
        ]

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector file with features to be clustered.")
        self.addParameter(input_vector_param)

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

        output_vector_param = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[3], description="Output vector"
        )
        output_vector_param.setHelp("Output vector file with new cluster label column.")
        self.addParameter(output_vector_param)
