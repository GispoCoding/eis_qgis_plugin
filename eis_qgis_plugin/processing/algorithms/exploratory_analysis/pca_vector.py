from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPcaVector(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "compute_pca_vector"
        self._display_name = "PCA (vector)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
            Compute PCA for vector data.

            Before computation, data is automatically standardized, and nodata values removed \
            or replaced with column mean.

            Either all or selected columns are used for PCA computation. Number of components should be at \
            least the total number of (selected) columns.
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

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input vector"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1],
                description="Number of components",
                defaultValue=3,
                minValue=2
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.alg_parameters[2],
                description="Columns",
                parentLayerParameterName=self.alg_parameters[0],
                allowMultiple=True,
                optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[3],
                description="Nodata handling",
                options=["remove", "replace"],
                defaultValue="remove"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[4],
                description="Nodata",
                type=QgsProcessingParameterNumber.Double,
                optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                name=self.alg_parameters[5], description="Output vector"
            )
        )
