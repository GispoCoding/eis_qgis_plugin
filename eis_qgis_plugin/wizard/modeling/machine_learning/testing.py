from typing import Iterable, List

from qgis import processing
from qgis.gui import QgsFileWidget, QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGroupBox,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.model_data_table import ModelDataTable
from eis_qgis_plugin.wizard.modeling.model_manager import ModelManager
from eis_qgis_plugin.wizard.modeling.model_utils import get_output_path, set_filter, set_placeholder_text

FORM_CLASS: QWidget = load_ui("modeling/testing.ui")



class EISMLModelTesting(QWidget, FORM_CLASS):

    ROW_HEIGHT = 26
    TESTING_ALG_NAME = "eis:evaluate_trained_model"
    
    def __init__(self, parent, model_main) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.model_main = model_main
        self.test_metrics = [  # IN ORDER
            self.accuracy_checkbox, self.precision_checkbox, self.recall_checkbox, self.f1_checkbox,
            self.auc_checkbox, self.mse_checkbox, self.rmse_checkbox, self.mae_checkbox, self.r2_checkbox
        ]

        # DECLARE TYPES
        self.test_model_selection: QComboBox
        self.model_file_testing: QLineEdit
        self.test_run_name: QLineEdit
        self.test_output_raster: QgsFileWidget

        self.test_evidence_data_layout: QVBoxLayout
        self.test_evidence_data_box: QGroupBox
        self.test_label_data: QgsMapLayerComboBox
        self.test_label_data_box: QGroupBox
        self.test_metrics_box: QGroupBox
        self.test_metrics_stack: QStackedWidget
        self.test_reset_btn: QPushButton
        self.test_run_btn: QPushButton

        self.accuracy_checkbox: QCheckBox
        self.precision_checkbox: QCheckBox
        self.recall_checkbox: QCheckBox
        self.f1_checkbox: QCheckBox
        self.auc_checkbox: QCheckBox
        self.mse_checkbox: QCheckBox
        self.rmse_checkbox: QCheckBox
        self.mae_checkbox: QCheckBox
        self.r2_checkbox: QCheckBox

        # Connect signals
        self.test_run_btn.clicked.connect(self.test_model)
        self.test_model_selection.currentTextChanged.connect(self._on_selected_model_changed)

        # Initialize
        self.test_evidence_data = ModelDataTable(self, self.ROW_HEIGHT)
        self.test_evidence_data_layout.addWidget(self.test_evidence_data)
       
        self.update_selectable_models(ModelManager.get_all_models())
        set_placeholder_text(self.test_output_raster)
        set_filter(self.test_output_raster, "raster")


    def _on_selected_model_changed(self, model_id: str):
        if model_id == "":
            self.test_evidence_data.load_model([])
            self.model_file_testing.setText("")
            return
        info = ModelManager.get_model_info(model_id)
        self.test_evidence_data.load_model(info["tags"])
        self.model_file_testing.setText(info["model_file"])


    def update_selectable_models(self, model_names: Iterable[str]):
        self.test_model_selection.clear()
        self.test_model_selection.addItems(model_names)


    def get_test_metrics(self) -> List[int]:
        metric_indices = []
        for i, checkbox in enumerate(self.test_metrics):
            if checkbox.isChecked():
                metric_indices.append(i)
        return metric_indices


    def test_model(self):
        processing.runAndLoadResults(
            self.TESTING_ALG_NAME,
            {
                "input_rasters": self.test_evidence_data.get_layers(),
                "target_labels": self.test_label_data.currentLayer(),
                "model_file": self.model_file_testing.text(),
                "validation_metrics": self.get_test_metrics(),
                "output_raster": get_output_path(self.test_output_raster)
            }
        )
