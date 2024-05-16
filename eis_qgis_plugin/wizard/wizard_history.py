from typing import Optional

from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils import clear_layout
from eis_qgis_plugin.wizard.modeling.ml_model_info import MLModelInfo
from eis_qgis_plugin.wizard.modeling.model_data_table import ModelHistoryTable
from eis_qgis_plugin.wizard.modeling.model_manager import ModelManager

FORM_CLASS: QDialog = load_ui("results/wizard_model_history.ui")


class EISWizardHistory(QWidget, FORM_CLASS): 

    ROW_HEIGHT = 26

    def __init__(self, parent=None, model_manager: ModelManager = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.model_manager = model_manager

        # DECLARE TYPES
        self.model_selection: QComboBox
        self.model_type: QLineEdit
        self.model_file: QLineEdit
        self.model_training_time: QLineEdit

        self.summary_data_box: QGroupBox
        self.evidence_data_box: QGroupBox
        self.evidence_data_layout: QVBoxLayout
        self.label_data_box: QGroupBox
        self.parameters_box: QGroupBox
        self.parameters_layout: QFormLayout

        self.label_layer_name: QLabel
        self.label_filepath: QLabel

        self.export_btn: QPushButton
        self.delete_btn: QPushButton
        self.delete_all_btn: QPushButton

        # Connect signals
        self.model_selection.currentTextChanged.connect(self.update_viewed_model)
        self.export_btn.clicked.connect(self._on_export_clicked)
        self.delete_btn.clicked.connect(self._on_delete_clicked)
        self.delete_all_btn.clicked.connect(self._on_delete_all_clicked)
        self.model_manager.models_updated.connect(self.update_list_of_models)

        # Initialize
        self.evidence_data = ModelHistoryTable(self, self.ROW_HEIGHT)
        self.evidence_data_layout.addWidget(self.evidence_data)

        self.update_list_of_models(0)


    def update_list_of_models(self, index: Optional[int] = None):
        models = ModelManager.get_all_models()
        self.model_selection.clear()
        self.model_selection.addItems(models)
        if index is not None:
            self.model_selection.setCurrentIndex(index)


    def update_viewed_model(self, model_id: str):
        info = ModelManager.get_model_info(model_id)
        if info is None:
            self.model_type.clear()
            self.model_file.clear()
        else:
            self.load_summary_data(info)
            self.load_evidence_data(info)
            self.load_label_data(info)
            self.load_parameter_data(info)


    def load_summary_data(self, info: MLModelInfo):
        self.model_type.setText(info.model_type)
        self.model_file.setText(info.model_file)
        self.model_training_time.setText(f"{str(round(info.training_time, 1))} s")

    def load_evidence_data(self, info: MLModelInfo):
        self.evidence_data.load_model(info.tags, info.evidence_data)

    def load_label_data(self, info: MLModelInfo):
        self.label_layer_name.setText(info.label_data[0])
        self.label_filepath.setText(info.label_data[1])

    def load_parameter_data(self, info: MLModelInfo):
        clear_layout(self.parameters_layout)
        for parameter_name, parameter_value in info.parameters.items():
            name_label = QLabel()
            name_label.setText(parameter_name)
            value_widget = QLineEdit()
            value_widget.setText(str(parameter_value))
            value_widget.setReadOnly(True)
            self.parameters_layout.addRow(name_label, value_widget)

    def _on_export_clicked(self):
        print("Model history exporting not implemented yet!")


    def _on_delete_clicked(self):
        model = self.model_selection.currentText()
        new_index = min(self.model_selection.currentIndex(), self.model_selection.count() - 2)
        self.model_manager.remove_model_info(model)
        self.update_list_of_models(index=new_index)
        print(f"Model {model} deleted")


    def _on_delete_all_clicked(self):
        self.model_manager.remove_model_info_all()
        self.update_list_of_models()
        print("All models deleted")