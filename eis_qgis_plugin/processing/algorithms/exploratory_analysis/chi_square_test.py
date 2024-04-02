from qgis.core import (
    QgsProcessingParameterField,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISChiSquareTest(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "chi_square_test"
        self._display_name = "Chi-square test"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
            Perform a Chi-square test of independence between a target variable and one or more other variables.

            Input data should be categorical data. Continuous data or non-categorical data should be discretized or \
            binned before using this function, as Chi-square tests are not applicable to continuous variables directly.

            The test assumes that the observed frequencies in each category are independent.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_vector", "target_column", "columns"]

        input_vector_param = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector file with features to be tested.")
        self.addParameter(input_vector_param)

        target_column_param = QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Target column",
            parentLayerParameterName=self.alg_parameters[0],
        )
        target_column_param.setHelp("Variable against which independence of other variables is tested.")
        self.addParameter(target_column_param)

        columns_param = QgsProcessingParameterField(
            name=self.alg_parameters[2],
            description="Other columns",
            allowMultiple=True,
            parentLayerParameterName=self.alg_parameters[0],
            optional=True
        )
        columns_param.setHelp(
            "Variables that are tested against the variable in target column. If not set, every column is used."
        )
        self.addParameter(columns_param)
