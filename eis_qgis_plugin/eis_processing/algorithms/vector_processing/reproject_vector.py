from qgis.core import (
    QgsProcessingParameterCrs,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISReprojectVector(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "reproject_vector"
        self._display_name = "Reproject vector"
        self._group = "Vector Processing"
        self._group_id = "vector_processing"
        self._short_help_string = "Reproject a vector layer"

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "target_crs", "output_vector"]

        reproject_vector_param = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[0], description="Input vector"
        )
        reproject_vector_param.setHelp("Input vector to reproject.")
        self.addParameter(reproject_vector_param)

        target_crs_param = QgsProcessingParameterCrs(
            name=self.alg_parameters[1], description="Target CRS"
        )
        target_crs_param.setHelp("The CRS of the reprojected vector.")
        self.addParameter(target_crs_param )

        output_vector_param = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[2], description="Output vector"
        )
        output_vector_param.setHelp("Output reprojected vector.")
        self.addParameter(output_vector_param)
