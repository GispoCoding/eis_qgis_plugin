from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPlotPrecisionRecallCurve(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "plot_precision_recall_curve"
        self._display_name = "Plot Precision-Recall curve"
        self._group = "Evaluation"
        self._group_id = "evaluation"
        self._short_help_string = """
        Plot precision-recall curve.

        Precision-recall curve is a binary classification multi-threshold metric. Precision-recall curve shows \
        the tradeoff between precision and recall for different classification thresholds. \
        It can be a useful measure of success when classes are imbalanced.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "true_labels",
            "probabilities",
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
                name=self.alg_parameters[1], description="Probabilities"
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
