from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterString,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPlotCorrelationMatrix(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "plot_correlation_matrix"
        self._display_name = "Plot correlation matrix"
        self._group = "Validation"
        self._group_id = "validation"
        self._short_help_string = "Create a heatmap to visualize correlation matrix."

    def initAlgorithm(self, config=None):
        #self.alg_parameters = ["matrix", "annotate", "cmap", "plot_title", "**kwargs", "out_raster"]
        self.alg_parameters = ["matrix", "annotate", "cmap", "plot_title", "out_raster"]

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                name=self.alg_parameters[0],
                description="Correlation matrix.",
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                name=self.alg_parameters[1],
                description="Plot squares display the correlation values."
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                name=self.alg_parameters[2],
                description="Color map",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                name=self.alg_parameters[3], description="Plot title",
                optional=True,
            )
        )

        # TODO! Need to think about how to allow the user to pass **kwargs.
        # self.addParameter(
            # QgsProcessingParameterEnum(
                # name=self.alg_parameters[4], description="Additional parameters to pass to Seaborn and matplotlib.",
            # )
        # )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[4], description="Output"
            )
        )
