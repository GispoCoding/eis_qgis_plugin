from typing import Iterable, List

from qgis import processing
from qgis.core import QgsProject, QgsRasterLayer
from qgis.gui import QgsDoubleSpinBox, QgsFileWidget, QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGroupBox,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils import add_output_layer_to_group
from eis_qgis_plugin.wizard.modeling.model_data_table import ModelDataTable
from eis_qgis_plugin.wizard.modeling.model_manager import ModelManager
from eis_qgis_plugin.wizard.modeling.model_utils import get_output_path, set_filter, set_placeholder_text
from eis_qgis_plugin.wizard.utils.model_feedback import EISProcessingFeedback
from eis_qgis_plugin.wizard.utils.settings_manager import EISSettingsManager

FORM_CLASS: QWidget = load_ui("modeling/testing.ui")



class EISMLModelTesting(QWidget, FORM_CLASS):

    ROW_HEIGHT = 26
    CLASSIFIER_ALG = "eis:classifier_test"
    REGRESSOR_ALG = "eis:regressor_test"

    def __init__(self, parent, model_main) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.model_main = model_main
        self.active_alg = self.CLASSIFIER_ALG
        self.model_info = None

        # METRICS IN ORDER MATCHIN PROCESSING ALGS
        self.classifier_metrics = [
            self.accuracy_checkbox, self.precision_checkbox, self.recall_checkbox, self.f1_checkbox,
        ]
        self.regressor_metrics = [self.mse_checkbox, self.rmse_checkbox, self.mae_checkbox, self.r2_checkbox]

        # DECLARE TYPES
        self.test_model_selection: QComboBox
        self.model_file_testing: QLineEdit
        self.test_run_name: QLineEdit
        self.test_output_raster_1: QgsFileWidget
        self.test_output_raster_label_1: QLabel
        self.test_output_raster_2: QgsFileWidget
        self.test_output_raster_label_2: QLabel

        self.test_evidence_data_layout: QVBoxLayout
        self.test_evidence_data_box: QGroupBox
        self.test_label_data: QgsMapLayerComboBox
        self.test_label_data_box: QGroupBox
        self.test_metrics_box: QGroupBox
        self.test_metrics_stack: QStackedWidget
        self.test_reset_btn: QPushButton
        self.test_run_btn: QPushButton

        self.test_parameter_box: QGroupBox
        self.test_classification_threshold: QgsDoubleSpinBox

        self.accuracy_checkbox: QCheckBox
        self.precision_checkbox: QCheckBox
        self.recall_checkbox: QCheckBox
        self.f1_checkbox: QCheckBox
        self.mse_checkbox: QCheckBox
        self.rmse_checkbox: QCheckBox
        self.mae_checkbox: QCheckBox
        self.r2_checkbox: QCheckBox

        self.testing_log: QTextEdit
        self.testing_progress_bar: QProgressBar

        # Connect signals
        self.test_run_btn.clicked.connect(self.test_model)
        self.test_model_selection.currentTextChanged.connect(self._on_selected_model_changed)

        # Initialize
        self.test_evidence_data = ModelDataTable(self, self.ROW_HEIGHT)
        self.test_evidence_data_layout.addWidget(self.test_evidence_data)
        self.testing_feedback = EISProcessingFeedback(self.testing_log, self.testing_progress_bar)
       
        self.update_selectable_models(ModelManager.get_all_models())
        set_placeholder_text(self.test_output_raster_1)
        set_placeholder_text(self.test_output_raster_2)
        set_filter(self.test_output_raster_1, "raster")
        set_filter(self.test_output_raster_2, "raster")


    def _on_selected_model_changed(self, model_id: str):
        if model_id == "":
            self.test_evidence_data.load_model([])
            self.model_file_testing.setText("")
            self.active_alg = self.CLASSIFIER_ALG
            self.model_info = None
            return
        self.model_info = ModelManager.get_model_info(model_id)
        self.test_evidence_data.load_model(self.model_info.tags)
        self.model_file_testing.setText(self.model_info.model_file)
        if self.model_info.model_kind == "classifier":
            self.active_alg = self.CLASSIFIER_ALG
            self.test_output_raster_label_2.show()
            self.test_output_raster_2.show()
            self.test_parameter_box.show()
            self.test_metrics_stack.setCurrentIndex(0)
            self.test_output_raster_label_1.setText("Output classified raster")
        else:
            self.active_alg = self.REGRESSOR_ALG
            self.test_output_raster_label_2.hide()
            self.test_output_raster_2.hide()
            self.test_parameter_box.hide()
            self.test_metrics_stack.setCurrentIndex(1)
            self.test_output_raster_label_1.setText("Output raster")


    def update_selectable_models(self, model_names: Iterable[str]):
        self.test_model_selection.clear()
        self.test_model_selection.addItems(model_names)


    def get_classifier_metrics(self) -> List[int]:
        metric_indices = []
        for i, checkbox in enumerate(self.classifier_metrics):
            if checkbox.isChecked():
                metric_indices.append(i)
        return metric_indices


    def get_regressor_metrics(self) -> List[int]:
        metric_indices = []
        for i, checkbox in enumerate(self.regressor_metrics):
            if checkbox.isChecked():
                metric_indices.append(i)
        return metric_indices


    def test_model(self):
        if self.model_info is None:
            return

        if self.model_info.model_kind == "classifier":
            result = processing.run(
                self.CLASSIFIER_ALG,
                {
                    "input_rasters": self.test_evidence_data.get_layers(),
                    "target_labels": self.test_label_data.currentLayer(),
                    "model_file": self.model_file_testing.text(),
                    "classification_threshold": self.test_classification_threshold.value(),
                    "test_metrics": self.get_classifier_metrics(),
                    "output_raster_probability": get_output_path(self.test_output_raster_2),
                    "output_raster_classified": get_output_path(self.test_output_raster_1)
                },
                feedback=self.testing_feedback
            )
            output_layers = [
                ("Output probabilities", "output_raster_probability"),
                ("Output classified", "output_raster_classified")
            ]
        elif self.model_info.model_kind == "regressor":
            result = processing.run(
                self.REGRESSOR_ALG,
                {
                    "input_rasters": self.test_evidence_data.get_layers(),
                    "target_labels": self.test_label_data.currentLayer(),
                    "model_file": self.model_file_testing.text(),
                    "validation_metrics": self.get_regressor_metrics(),
                    "output_raster": get_output_path(self.test_output_raster_1)
                },
                feedback=self.testing_feedback
            )
            output_layers = [("Output predictions", "output_raster")]
        else:
            print(f"Unknown model kind: {self.model_info.model_kind}")
            return

        for (layer_name, output_layer) in output_layers:
            layer = QgsRasterLayer(result[output_layer], layer_name)
            if EISSettingsManager.get_layer_group_selection():
                add_output_layer_to_group(
                    layer, f"Modeling — {self.model_info.model_type}", self.model_info.model_instance_name
                )
            else:
                QgsProject.instance().addMapLayer(layer, True)
