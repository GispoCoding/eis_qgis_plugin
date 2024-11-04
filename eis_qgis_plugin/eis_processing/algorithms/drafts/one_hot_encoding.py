from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterEnum,
    QgsProcessingParameterField,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterMapLayer,
    QgsProcessingParameterNumber,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISOneHotEncoding(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "one_hot_encoding"
        self._display_name = "One hot encoding"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = (
            " Perform one-hot (or one-of-K or dummy) encoding on categorical data"
        )

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_data",
            "columns",
            "drop_columns",
            "drop_category",
            "sparse_output",
            "out_dtype",
            "handle_unknown",
            "min_frequency",
            "max_categories",
            "output_file"
            ]

        self.addParameter(
            QgsProcessingParameterMapLayer(
                name=self.alg_parameters[0], description="Input file"
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.alg_parameters[1],
                description="Target columns (for vector layers)",
                allowMultiple=True,
                optional=True,
                defaultValue=None
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                name=self.alg_parameters[2],
                description="Drop original columns",
                defaultValue=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[3],
                description="Drop category",
                options=["first", "if_binary"],
                defaultValue=None,
                optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                name=self.alg_parameters[4],
                description="Sparse output",
                defaultValue=True
            )
        )

        # Maybe this should be an Enum?
        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[5],
                description="output dtype",
                options=["int", "float"]
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[6],
                description="Handle unknown",
                options=["error", "ignore", "infrequent_if_exist"],
                defaultValue="infrequent_if_exist",
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[7],
                description="Min frequency",
                type=QgsProcessingParameterNumber.Double,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[8],
                description="Max categories",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[9],
                description="Output file"
            )
        )
