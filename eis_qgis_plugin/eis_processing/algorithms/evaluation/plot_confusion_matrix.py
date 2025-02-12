from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPlotConfusionMatrix(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "plot_confusion_matrix"
        self._display_name = "Plot confusion matrix"
        self._group = "Evaluation"
        self._group_id = "evaluation"
        self._short_help_string = """
        Plot confusion matrix.

        A confusion matrix is a heatmap used to evaluate the classification results. It compares true labels (y-axis) \
        with the predicted labels (x-axis) correctly predicted labels being on the diagonal.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "true_labels",
            "predictions",
            "show_plot",
            "save_dpi",
            "output_file"
        ]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0],
                description="True labels",
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[1], description="Predictions"
            )
        )

        show_plot_param = QgsProcessingParameterBoolean(
            name=self.alg_parameters[2], description="Show plot immediately", defaultValue=True
        )
        show_plot_param.setHelp(
            "If the produced plot should be displayed immediately. Note that the algorithm " +
            "does not finish before the popup window is closed."
        )
        self.addParameter(show_plot_param)

        save_dpi_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            description="Save dpi",
            optional=True,
            minValue=1
        )
        save_dpi_param.setHelp(
            "Controls the resolution of the plot. Higher values will lead to more detailed plots. " +
            "If not set, the underlying plot library determines the output dpi."
        )
        self.addParameter(save_dpi_param)

        output_file_param = QgsProcessingParameterFileDestination(
            name=self.alg_parameters[4],
            description="Output file",
            fileFilter='PNG files (*.png);;JPEG files (*.jpg *.jpeg);;PDF files (*.pdf);;SVG files (*.svg)'
        )
        output_file_param.setHelp("The output plot file.")
        self.addParameter(output_file_param)
