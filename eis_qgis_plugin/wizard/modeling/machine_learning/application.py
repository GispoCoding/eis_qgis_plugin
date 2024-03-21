from typing import Iterable

from qgis import processing
from qgis.gui import QgsFileWidget
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QGroupBox,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.model_data_table import ModelDataTable
from eis_qgis_plugin.wizard.modeling.model_manager import ModelManager
from eis_qgis_plugin.wizard.modeling.model_utils import get_output_path, set_filter, set_placeholder_text

FORM_CLASS: QWidget = load_ui("modeling/application.ui")



class EISMLModelApplication(QWidget, FORM_CLASS):
    """Parent class for ML model classes in EIS Wizard."""

    ROW_HEIGHT = 26
    PREDICTION_ALG_NAME = "eis:predict_with_trained_model"
    
    def __init__(self, parent, model_main) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.model_main = model_main

        # DECLARE TYPES
        self.application_model_selection: QComboBox
        self.model_file_application: QLineEdit
        self.application_run_name: QLineEdit
        self.application_output_raster: QgsFileWidget

        self.application_evidence_data_layout: QVBoxLayout
        self.application_evidence_data_box: QGroupBox
        self.application_reset_btn: QPushButton
        self.application_run_btn: QPushButton

        # Connect signals
        self.application_run_btn.clicked.connect(self.apply_model)
        self.application_model_selection.currentTextChanged.connect(self._on_selected_model_changed)

        # Initialize
        self.application_evidence_data = ModelDataTable(self, self.ROW_HEIGHT)
        self.application_evidence_data_layout.addWidget(self.application_evidence_data)

        self.update_selectable_models(ModelManager.get_all_models())
        set_placeholder_text(self.application_output_raster)
        set_filter(self.application_output_raster, "raster")


    def _on_selected_model_changed(self, model_key: str):
        if model_key == "":
            self.application_evidence_data.load_model([])
            self.model_file_application.setText("")
            return
        info = ModelManager.get_model_info(model_key)
        self.application_evidence_data.load_model(info["tags"])
        self.model_file_application.setText(info["model_file"])


    def update_selectable_models(self, model_names: Iterable[str]):
        self.application_model_selection.clear()
        self.application_model_selection.addItems(model_names)


    def apply_model(self):
        processing.runAndLoadResults(
            self.PREDICTION_ALG_NAME,
            {
                "input_rasters": self.application_evidence_data.get_layers(),
                "model_file": self.model_file_application.text(),
                "output_raster": get_output_path(self.application_output_raster)
            }
        )
