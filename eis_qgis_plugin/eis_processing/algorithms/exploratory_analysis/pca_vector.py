from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPcaVector(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "compute_pca_vector"
        self._display_name = "PCA (vector)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
            Compute PCA (principal component analysis) for vector data.

            Before computation, data is automatically standardized, and nodata values removed \
            or replaced with column mean.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_vector",
            "number_of_components",
            "columns",
            "nodata_handling",
            "nodata",
            "output_vector"
        ]

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector file to be used for PCA.")
        self.addParameter(input_vector_param)

        nr_of_components_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Number of components",
            defaultValue=3,
            minValue=2
        )
        nr_of_components_param.setHelp(
            "Number of principal components to compute. Number of components should be at \
            least the total number of (selected) columns. "
        )
        self.addParameter(nr_of_components_param)

        columns_param = QgsProcessingParameterField(
            name=self.alg_parameters[2],
            description="Columns",
            parentLayerParameterName=self.alg_parameters[0],
            allowMultiple=True,
            optional=True
        )
        columns_param.setHelp(
            "Columns used for the PCA. If not defined, all columns will be used. \
            Unselected columns are excluded from PCA, but added back to the result vector file intact. \
            Used columns are consumed."
        )
        self.addParameter(columns_param)

        nodata_handling_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[3],
            description="Nodata handling",
            options=["remove", "replace"],
            defaultValue="remove"
        )
        nodata_handling_param.setHelp(
            "If features with nodata should be removed for the time of PCA computation or replaced with column means."
        )
        self.addParameter(nodata_handling_param)

        nodata_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4],
            description="Nodata",
            type=QgsProcessingParameterNumber.Double,
            optional=True
        )
        nodata_param.setHelp(
            "Additional nodata value definition. NULL/NaN values are handled automatically."
        )
        self.addParameter(nodata_param)

        output_vector_param = QgsProcessingParameterVectorDestination(
            name=self.alg_parameters[5], description="Output vector"
        )
        output_vector_param.setHelp(
            "Output vector file with columns for each principal component."
        )
        self.addParameter(output_vector_param)
