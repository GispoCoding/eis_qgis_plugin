from qgis.core import QgsApplication, QgsMapLayerProxyModel
from qgis.gui import QgsMapLayerComboBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QDialogButtonBox,
    QProgressBar,
    QTextEdit,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.algorithm_execution import AlgorithmExecutor
from eis_qgis_plugin.utils.model_feedback import EISProcessingFeedback

FORM_CLASS: QWidget = load_ui("modeling/conditional_independence_test.ui")


class EISWofeConditionalIndependence(QWidget, FORM_CLASS):
    """Weights of evidence conditional independence step."""

    ALG_NAME = "eis:agterberg_cheng_ci_test"

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # TYPES
        self.posterior_probabilities: QgsMapLayerComboBox
        self.posterior_probabilities_std: QgsMapLayerComboBox
        self.weights_table: QgsMapLayerComboBox

        self.progress_bar: QProgressBar
        self.log: QTextEdit
        self.button_box: QDialogButtonBox

        # INIT
        self.posterior_probabilities.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.posterior_probabilities_std.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.weights_table.setFilters(QgsMapLayerProxyModel.NoGeometry)

        self.run_btn = self.button_box.button(QDialogButtonBox.Ok)
        self.run_btn.setText("Run")
        self.run_btn.setIcon(QIcon(QgsApplication.getThemeIcon("mActionStart.svg")))
        self.run_btn.clicked.connect(self.run)
        self.cancel_btn = self.button_box.button(QDialogButtonBox.Cancel)
        self.cancel_btn.clicked.connect(self.cancel)

        self.feedback = EISProcessingFeedback(text_edit=self.log, progress_bar=self.progress_bar)

        self.executor = AlgorithmExecutor()
        self.executor.finished.connect(self.on_algorithm_executor_finished)
        self.executor.terminated.connect(self.on_algorithm_executor_terminated)
        self.executor.error.connect(self.on_algorithm_executor_error)


    def run(self):
        params = {
            "input_posterior_probabilities": self.posterior_probabilities.currentLayer(),
            "input_posterior_probabilities_std": self.posterior_probabilities.currentLayer(),
            "input_weights_table": self.weights_table.currentLayer(),
        }
        self.executor.configure(self.ALG_NAME, self.feedback)
        self.executor.run(params)


    def on_algorithm_executor_finished(self, result, _):
        if self.feedback.no_errors:
            pass


    def on_algorithm_executor_error(self, error_message: str):
        pass


    def on_algorithm_executor_terminated(self):
        self.feedback = EISProcessingFeedback(text_edit=self.log, progress_bar=self.progress_bar)


    def cancel(self):
        if self.executor is not None:
            self.executor.cancel()
