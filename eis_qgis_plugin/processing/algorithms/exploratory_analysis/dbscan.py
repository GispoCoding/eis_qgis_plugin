from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISDbscan(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "dbscan"
        self._display_name = "DBSCAN"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Perform DBSCAN clustering on the input vector data."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_vector",
            "max_distance",
            "min_samples",
            "output_vector",
        ]

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector file with features to be clustered.")
        self.addParameter(input_vector_param)

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

        output_vector_param = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[3], description="Output vector"
        )
        output_vector_param.setHelp(
            "Output vector file with 2 new columns: cluster label and core point column (1 = core point).")
        self.addParameter(output_vector_param)
