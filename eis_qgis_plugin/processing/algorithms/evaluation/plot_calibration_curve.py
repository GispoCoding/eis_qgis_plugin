from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISPlotCalibrationCurve(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "plot_calibration_curve"
        self._display_name = "Plot calibration curve"
        self._group = "Evaluation"
        self._group_id = "evaluation"
        self._short_help_string = """
        Plot calibration curve (aka realibity diagram).

        Calibration curve has the frequency of the positive labels on the y-axis and the predicted probability on \
        the x-axis. Generally, the close the calibration curve is to line x=y, the better the model is calibrated.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "true_labels",
            "probabilities",
            "n_bins",
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

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2], description="N bins", defaultValue=5
            )
        )

        show_plot_param = QgsProcessingParameterBoolean(
            name=self.alg_parameters[3], description="Show plot immediately"
        )
        show_plot_param.setHelp(
            "If the produced plot should be displayed immediately. Note that the algorithm " +
            "does not finish before the popup window is closed."
        )
        self.addParameter(show_plot_param)

        save_dpi_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4],
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
            name=self.alg_parameters[5],
            description="Output file",
            fileFilter='PNG files (*.png);;JPEG files (*.jpg *.jpeg);;PDF files (*.pdf);;SVG files (*.svg)'
        )
        output_file_param.setHelp("The output plot file.")
        self.addParameter(output_file_param)
