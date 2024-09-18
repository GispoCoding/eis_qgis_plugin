from qgis.core import (
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISCellBasedAssociation(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "cell_based_association"
        self._display_name = "Cell based association"
        self._group = "Vector processing"
        self._group_id = "vector_processing"
        self._short_help_string = "Creation of CBA matrix."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_vector",
            "cell_size",
            "columns",
            # "subset_target_attribute_values",
            "add_name",
            "add_buffer",
            "output_vector"
        ]

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                name=self.alg_parameters[0],
                description="Input vector",
                allowMultiple=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[1], description="Cell size",
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                name=self.alg_parameters[2],
                description="Columns name",
                multiLine=True
            )
        )

        # No idea how to implement this
        # subset_target_attribute_values: Optional[List[Union[None, list, str]]] = None,
        # self.addParameter(
            # QgsProcessingParameter(
                # name=self.alg_parameters[3],
                # description="Subset target attribute values",
                # optional=True,
                # defaultValue=None
            # )
        # )

        self.addParameter(
            QgsProcessingParameterString(
                name=self.alg_parameters[3],
                description="Add column",
                optional=True,
                defaultValue=None,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[4],
                description="Add buffer",
                type=QgsProcessingParameterNumber.Double,
                optional=True,
                defaultValue=None
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                name=self.alg_parameters[5],
                description="Output",
            )
        )
