from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterString,
    QgsProcessingParameterColor,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFileDestination
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISParallelCoordinates(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "parallel_coordinates"
        self._display_name = "Plot parallel coordinates"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = "Generate a parallel coordinates plot."

    def initAlgorithm(self, config=None):

        self.alg_parameters = [
            "input_vector",
            "color_column_name",
            "plot_title",
            "palette",
            "curved_lines",
            "show_plot",
            "output_file"
        ]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.alg_parameters[0], description="Input vector"
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.alg_parameters[1],
                description="Color column",
                parentLayerParameterName=self.alg_parameters[0],
                optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                name=self.alg_parameters[2],
                description="Plot title",
                optional=True
            )
        )

        self.addParameter(  #TODO Modify
            QgsProcessingParameterColor(
                name=self.alg_parameters[3],
                description="Palette",
                optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                name=self.alg_parameters[4], description="Curved lines"
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                name=self.alg_parameters[5], description="Show plot"
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[6], description="Output file", optional=True
            )
        )
