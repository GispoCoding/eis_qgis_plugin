from qgis.core import QgsApplication, QgsMapLayerProxyModel, QgsProject, QgsRasterLayer
from qgis.gui import QgsFileWidget, QgsMapLayerComboBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QDialogButtonBox,
    QProgressBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from eis_qgis_plugin.eis_wizard.modeling.model_data_table import ModelTrainingDataTable
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.algorithm_execution import AlgorithmExecutor
from eis_qgis_plugin.utils.misc_utils import (
    add_output_layer_to_group,
    # apply_color_ramp_to_raster_layer,
    get_output_layer_name,
    get_output_path,
    set_placeholder_text,
)
from eis_qgis_plugin.utils.model_feedback import EISProcessingFeedback
from eis_qgis_plugin.utils.settings_manager import EISSettingsManager

FORM_CLASS: QWidget = load_ui("modeling/calculate_responses.ui")



class EISWofeCalculateResponses(QWidget, FORM_CLASS):
    """Weights of evidence calculate responses step."""

    ALG_NAME = "eis:weights_of_evidence_calculate_responses"

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # TYPES
        self.weight_rasters_layout: QVBoxLayout
        self.standard_deviation_rasters_layout: QVBoxLayout
        self.weights_table: QgsMapLayerComboBox

        self.output_probabilities: QgsFileWidget
        self.output_probabilities_std: QgsFileWidget
        self.output_confidence: QgsFileWidget

        self.progress_bar: QProgressBar
        self.log: QTextEdit
        self.button_box: QDialogButtonBox

        # INIT
        self.weight_rasters_table = ModelTrainingDataTable(self, add_tag_column=False)
        self.weight_rasters_table.setToolTip("Weight rasters")
        self.weight_rasters_layout.addWidget(self.weight_rasters_table)

        self.weight_std_rasters_table = ModelTrainingDataTable(self, add_tag_column=False)
        self.weight_rasters_table.setToolTip("Standard deviation rasters")
        self.standard_deviation_rasters_layout.addWidget(self.weight_std_rasters_table)

        self.weights_table.setFilters(QgsMapLayerProxyModel.NoGeometry)

        set_placeholder_text(self.output_probabilities, "[Save to temporary file]")
        set_placeholder_text(self.output_probabilities_std, "[Save to temporary file]")
        set_placeholder_text(self.output_confidence, "[Save to temporary file]")

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

        self.output_layers = [
            ("Posterior probabilities", "output_probabilities", self.output_probabilities),
            ("Posterior probabilities std", "output_probabilities_std", self.output_probabilities_std),
            ("Posterior probabilities confidence", "output_confidence_array", self.output_confidence)
        ]


    def run(self):
        params = {
            "input_rasters_weights": self.weight_rasters_table.get_layers(),
            "input_rasters_standard_deviations": self.weight_std_rasters_table.get_layers(),
            "input_weights_table": self.weights_table.currentLayer(),
            "output_probabilities": get_output_path(self.output_probabilities),
            "output_probabilities_std": get_output_path(self.output_probabilities_std),
            "output_confidence_array": get_output_path(self.output_confidence),
        }
        self.executor.configure(self.ALG_NAME, self.feedback)
        self.executor.run(params)


    def on_algorithm_executor_finished(self, result, _):
        if self.feedback.no_errors:

            # Load output rasters
            for (layer_name, output_layer, output_path) in self.output_layers:
                layer = QgsRasterLayer(result[output_layer], get_output_layer_name(output_path, layer_name))
                if EISSettingsManager.get_layer_group_selection():
                    add_output_layer_to_group(
                        layer, "Modeling — Weights of evidence", "Responses"
                    )
                else:
                    QgsProject.instance().addMapLayer(layer, True)

                # apply_color_ramp_to_raster_layer(layer, EISSettingsManager.get_raster_color_ramp())


    def on_algorithm_executor_error(self, error_message: str):
        pass


    def on_algorithm_executor_terminated(self):
        self.feedback = EISProcessingFeedback(text_edit=self.log, progress_bar=self.progress_bar)


    def cancel(self):
        if self.executor is not None:
            self.executor.cancel()
