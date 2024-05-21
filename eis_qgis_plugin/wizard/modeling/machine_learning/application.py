from typing import Iterable

from qgis import processing
from qgis.core import QgsProject, QgsRasterLayer
from qgis.gui import QgsDoubleSpinBox, QgsFileWidget
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QGroupBox,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
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

FORM_CLASS: QWidget = load_ui("modeling/application.ui")



class EISMLModelApplication(QWidget, FORM_CLASS):
    """Parent class for ML model classes in EIS Wizard."""

    ROW_HEIGHT = 26
    CLASSIFIER_ALG = "eis:classifier_predict"
    REGRESSOR_ALG = "eis:regressor_predict"
    
    def __init__(self, parent, model_main) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.model_main = model_main
        self.model_info = None

        # DECLARE TYPES
        self.application_model_selection: QComboBox
        self.model_file_application: QLineEdit
        self.application_run_name: QLineEdit
        self.application_output_raster_1: QgsFileWidget
        self.application_output_raster_label_1: QLabel
        self.application_output_raster_2: QgsFileWidget
        self.application_output_raster_label_2: QLabel

        self.application_evidence_data_layout: QVBoxLayout
        self.application_evidence_data_box: QGroupBox
        self.application_reset_btn: QPushButton
        self.application_run_btn: QPushButton

        self.application_parameter_box: QGroupBox
        self.application_classification_threshold: QgsDoubleSpinBox

        self.application_log: QTextEdit
        self.application_progress_bar: QProgressBar

        # Connect signals
        self.application_run_btn.clicked.connect(self.apply_model)
        self.application_model_selection.currentTextChanged.connect(self._on_selected_model_changed)

        # Initialize
        self.application_evidence_data = ModelDataTable(self, self.ROW_HEIGHT)
        self.application_evidence_data_layout.addWidget(self.application_evidence_data)
        self.application_feedback = EISProcessingFeedback(self.application_log, self.application_progress_bar)

        self.update_selectable_models(ModelManager.get_all_models())
        set_placeholder_text(self.application_output_raster_1)
        set_placeholder_text(self.application_output_raster_2)
        set_filter(self.application_output_raster_1, "raster")
        set_filter(self.application_output_raster_2, "raster")


    def _on_selected_model_changed(self, model_key: str):
        if model_key == "":
            self.application_evidence_data.load_model([])
            self.model_file_application.setText("")
            self.model_info = None
            return
        self.model_info = ModelManager.get_model_info(model_key)
        self.application_evidence_data.load_model(self.model_info.tags)
        self.model_file_application.setText(self.model_info.model_file)
        if self.model_info.model_kind == "classifier":
            self.application_output_raster_label_2.show()
            self.application_output_raster_2.show()
            self.application_parameter_box.show()
            self.application_output_raster_label_1.setText("Output classified raster")
        else:
            self.application_output_raster_label_2.hide()
            self.application_output_raster_2.hide()
            self.application_parameter_box.hide()
            self.application_output_raster_label_1.setText("Output raster")


    def update_selectable_models(self, model_names: Iterable[str]):
        self.application_model_selection.clear()
        self.application_model_selection.addItems(model_names)


    def apply_model(self):
        if self.model_info is None:
            return

        if self.model_info.model_kind == "classifier":
            result = processing.run(
                self.CLASSIFIER_ALG,
                {
                    "input_rasters": self.application_evidence_data.get_layers(),
                    "model_file": self.model_file_application.text(),
                    "classification_threshold": self.application_classification_threshold.value(),
                    "output_raster_probability": get_output_path(self.application_output_raster_2),
                    "output_raster_classified": get_output_path(self.application_output_raster_1)
                },
                feedback=self.application_feedback
            )
            output_layers = [
                ("Output probabilities", "output_raster_probability"),
                ("Output classified", "output_raster_classified")
            ]
        elif self.model_info.model_kind == "regressor":
            result = processing.run(
                self.REGRESSOR_ALG,
                {
                    "input_rasters": self.application_evidence_data.get_layers(),
                    "model_file": self.model_file_application.text(),
                    "output_raster": get_output_path(self.application_output_raster_1)
                },
                feedback=self.application_feedback
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
        
