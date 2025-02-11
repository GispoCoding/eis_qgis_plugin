from qgis.core import QgsApplication, QgsMapLayerProxyModel, QgsProject, QgsRasterLayer, QgsVectorLayer
from qgis.gui import QgsCheckableComboBox, QgsDoubleSpinBox, QgsFileWidget, QgsMapLayerComboBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialogButtonBox,
    QProgressBar,
    QTextEdit,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.algorithm_execution import AlgorithmExecutor
from eis_qgis_plugin.utils.misc_utils import (
    add_output_layer_to_group,
    apply_color_ramp_to_raster_layer,
    get_output_path,
    set_filter,
    set_placeholder_text,
)
from eis_qgis_plugin.utils.model_feedback import EISProcessingFeedback
from eis_qgis_plugin.utils.settings_manager import EISSettingsManager

FORM_CLASS: QWidget = load_ui("modeling/calculate_weights.ui")



class EISWofeCalculateWeights(QWidget, FORM_CLASS):
    """Weights of evidence calculate weights step."""

    ALG_NAME = "eis:weights_of_evidence_calculate_weights"

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # TYPES
        self.evidential_raster: QgsMapLayerComboBox
        self.deposits: QgsMapLayerComboBox

        self.weights_type: QComboBox
        self.studentized_contrast_threshold: QgsDoubleSpinBox
        self.rasters_to_generate: QgsCheckableComboBox

        self.output_table: QgsFileWidget
        self.output_directory: QgsFileWidget

        self.progress_bar: QProgressBar
        self.log: QTextEdit
        self.button_box: QDialogButtonBox

        # INIT
        self.evidential_raster.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.deposits.setFilters(QgsMapLayerProxyModel.RasterLayer | QgsMapLayerProxyModel.PointLayer)
        set_filter(self.output_table, "csv")
        set_placeholder_text(self.output_table, "[Save to temporary file]")
        set_placeholder_text(self.output_directory, "[Save to temporary folder]")

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

        self.raster_items = [
            "Class",
            "Pixel count",
            "Deposit count",
            "W+",
            "S_W+",
            "W–",
            "S_W–",
            "Contrast",
            "S_Contrast",
            "Studentized contrast",
            "Generalized class",
            "Generalized W+",
            "Generalized S_W+"
        ]
        self.rasters_to_generate.addItems(self.raster_items)


    def run(self):
        params = {
            "evidential_raster": self.evidential_raster.currentLayer(),
            "deposits": self.deposits.currentLayer(),
            "weights_type": self.weights_type.currentIndex(),
            "studentized_contrast_threshold": self.studentized_contrast_threshold.value(),
            "arrays_to_generate": [self.raster_items.index(item) for item in self.rasters_to_generate.checkedItems()],
            "output_results_table": get_output_path(self.output_table),  # Check param name
            "output_raster_dir": get_output_path(self.output_directory)
        }
        self.executor.configure(self.ALG_NAME, self.feedback)
        self.executor.run(params)


    def on_algorithm_executor_finished(self, result, _):
        if self.feedback.no_errors:
            # Load weights table
            table_layer = QgsVectorLayer(result["output_results_table"], "Weights table")
            add_output_layer_to_group(
                table_layer, "Modeling — Weights of evidence", "Weights"
            )

            # Load output rasters
            for (layer_name, output_path) in result["output_folder_rasters"].items():
                layer = QgsRasterLayer(output_path, layer_name)
                if EISSettingsManager.get_layer_group_selection():
                    add_output_layer_to_group(
                        layer, "Modeling — Weights of evidence", "Weights"
                    )
                else:
                    QgsProject.instance().addMapLayer(layer, True)

                apply_color_ramp_to_raster_layer(layer, EISSettingsManager.get_raster_color_ramp())


    def on_algorithm_executor_error(self, error_message: str):
        pass


    def on_algorithm_executor_terminated(self):
        self.feedback = EISProcessingFeedback(text_edit=self.log, progress_bar=self.progress_bar)


    def cancel(self):
        if self.executor is not None:
            self.executor.cancel()
