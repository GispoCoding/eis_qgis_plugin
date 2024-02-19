from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterEnum,    
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISLocalMoransI(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "local_morans_i"
        self._display_name = "Local Moran's I"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = (
            "Perform Local Moran's I calculation."
        )

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_vector",
            "output_vector",
            "column",
            "weight_type",
            "k",
            "permutations",
        ]

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0],
            description="Input geometries"
        )
        input_vector_param.setHelp("Input geometries that contains the data to be examined with Local Moran's I.")
        self.addParameter(input_vector_param)

        output_vector_param = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[1],
            description="Output geometries"
        )
        output_vector_param.setHelp("Output for Local Moran's I calculation.")
        self.addParameter(output_vector_param)

        column_param = QgsProcessingParameterField(
            name=self.alg_parameters[2],
            description="Column",
            parentLayerParameterName=self.alg_parameters[0]
        )
        column_param.setHelp("The column to be used in the analysis.")
        self.addParameter(column_param)

        weight_type_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[3],
            description="Weight type",
            options=["queen", "knn"],
            defaultValue="queen"
        )
        weight_type_param.setHelp("The type of spatial weights matrix to be used. Defaults to queen.")
        self.addParameter(weight_type_param)

        k_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4],
            description="k",
            defaultValue="4"
        )
        k_param.setHelp("Number of nearest neighbors for the KNN weights matrix. Defaults to 4.")
        self.addParameter(k_param)

        permutations_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[5],
            description="Permutations",
            defaultValue="999"
        )
        permutations_param.setHelp("Number of permutations for significance testing. Defaults to 999.")
        self.addParameter(permutations_param)

