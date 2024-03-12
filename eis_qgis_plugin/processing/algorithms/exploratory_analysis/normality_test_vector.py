from qgis.core import QgsProcessingParameterField, QgsProcessingParameterVectorLayer

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISNormalityTestVector(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "normality_test_vector"
        self._display_name = "Normality test (vector)"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
        Compute Shapiro-Wilk normality test on input vector data.

        Normality is calculated for each attribute separately.
        Nodata values are automatically ignored.
        
        Displays Shapiro-Wilk statistics and p-values as a result.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "columns"]

        input_vector_param = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector data containing attributes to be tested.")
        self.addParameter(input_vector_param)

        columns_param = QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Columns",
            parentLayerParameterName=self.alg_parameters[0],
            allowMultiple=True,
            optional=True
        )
        columns_param.setHelp(
            "Column selection. Selected columns should be numeric. " + 
            "If not provided, normality is tested for all numeric columns."
        )
        self.addParameter(columns_param)
