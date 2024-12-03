from typing import Optional

from qgis.core import QgsApplication
from qgis.gui import QgsFileWidget
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from eis_qgis_plugin.eis_wizard.modeling.ml_model_info import MLModelInfo
from eis_qgis_plugin.eis_wizard.modeling.model_data_table import ModelHistoryTable
from eis_qgis_plugin.eis_wizard.modeling.model_manager import ModelManager
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.message_manager import EISMessageManager
from eis_qgis_plugin.utils.misc_utils import clear_layout, set_filter

FORM_CLASS: QDialog = load_ui("wizard_model_history.ui")


class EISWizardHistory(QWidget, FORM_CLASS): 

    ROW_HEIGHT = 26

    def __init__(self, parent=None, model_manager: ModelManager = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.model_manager = model_manager

        # DECLARE TYPES
        self.model_selection: QComboBox
        self.model_type: QLineEdit
        self.model_file: QgsFileWidget
        self.model_file_label: QLabel
        self.update_model_file_btn: QPushButton
        self.model_training_date: QLineEdit
        self.model_training_time: QLineEdit

        self.summary_data_box: QGroupBox
        self.evidence_data_box: QGroupBox
        self.evidence_data_layout: QVBoxLayout
        self.label_data_box: QGroupBox
        self.parameters_box: QGroupBox
        self.parameters_layout: QFormLayout

        self.label_layer_name: QLabel
        self.label_filepath: QLabel

        self.button_box: QDialogButtonBox
        self.export_btn: QPushButton
        self.delete_btn: QPushButton
        self.delete_all_btn: QPushButton

        self.active_info: Optional[MLModelInfo]

        # Initialize and connect signals
        self.model_selection.currentTextChanged.connect(self.update_viewed_model)
        self.update_model_file_btn.clicked.connect(self.update_model_file)
        self.update_model_file_btn.setIcon(QIcon(QgsApplication.getThemeIcon("mActionSaveAllEdits.svg")))
        self.update_model_file_btn.setToolTip(
            "If your model file name or path has changed, you can change and update it."
        )

        self.delete_all_btn = self.button_box.addButton("Delete all", QDialogButtonBox.ActionRole)
        self.delete_all_btn.setIcon(QIcon(QgsApplication.getThemeIcon("mActionDeleteSelected.svg")))
        self.delete_all_btn.clicked.connect(self._on_delete_all_clicked)

        self.delete_btn = self.button_box.addButton("Delete", QDialogButtonBox.ActionRole)
        self.delete_btn.setIcon(QIcon(QgsApplication.getThemeIcon("mActionDeleteSelected.svg")))
        self.delete_btn.clicked.connect(self._on_delete_clicked)

        self.export_btn = self.button_box.addButton("Export", QDialogButtonBox.ActionRole)
        self.export_btn.setIcon(QIcon(QgsApplication.getThemeIcon('mActionFileSaveAs.svg')))
        self.export_btn.clicked.connect(self._on_export_clicked)

        self.model_manager.models_updated.connect(self.update_list_of_models)
        
        self.evidence_data = ModelHistoryTable(self, self.ROW_HEIGHT)
        self.evidence_data_layout.addWidget(self.evidence_data)
        set_filter(self.model_file, "joblib")

        self.update_list_of_models(0)


    def update_list_of_models(self, index: Optional[int] = None):
        models = ModelManager.get_all_models()
        self.model_selection.clear()
        self.model_selection.addItems(models)
        if index is not None:
            self.model_selection.setCurrentIndex(index)


    def update_viewed_model(self, model_id: str):
        info = ModelManager.get_model_info(model_id)
        self.active_info = info
        if info is None:
            self.clear_summary_data()
            self.clear_evidence_data()
            self.clear_label_data()
            self.clear_parameter_data()
        else:
            if not info.check_model_file():
                self.model_file_label.setText("Model file (MISSING!)")
            else:
                self.model_file_label.setText("Model file")
            self.load_summary_data(info)
            self.load_evidence_data(info)
            self.load_label_data(info)
            self.load_parameter_data(info)


    def update_model_file(self):
        index = self.model_selection.currentIndex()
        model_name = self.model_selection.currentText()
        if self.active_info is not None:
            self.active_info.update(model_file=self.model_file.filePath())
            self.model_manager.save_model_info(self.active_info)
        # Make sure the viewed model does not change after model file update
        self.update_list_of_models(index)
        EISMessageManager().show_message(f"Model file path for {model_name} updated.", "success")


    def load_summary_data(self, info: MLModelInfo):
        self.model_type.setText(info.model_type)
        self.model_file.setFilePath(info.model_file)
        self.model_training_date.setText(info.training_date)
        self.model_training_time.setText(f"{str(round(info.training_time, 1))} s")


    def load_evidence_data(self, info: MLModelInfo):
        self.evidence_data.load_model(info.tags, info.evidence_data)


    def load_label_data(self, info: MLModelInfo):
        self.label_layer_name.setText(info.label_data[0])
        self.label_filepath.setText(info.label_data[1])


    def load_parameter_data(self, info: MLModelInfo):
        self.clear_parameter_data()
        for parameter_name, parameter_value in info.parameters.items():
            name_label = QLabel()
            name_label.setText(parameter_name)
            value_widget = QLineEdit()
            value_widget.setText(str(parameter_value))
            value_widget.setReadOnly(True)
            self.parameters_layout.addRow(name_label, value_widget)


    def clear_summary_data(self):
        self.model_type.clear()
        self.model_file.setFilePath("")
        self.model_training_date.clear()
        self.model_training_time.clear()


    def clear_evidence_data(self):
        self.evidence_data.reset_table()


    def clear_label_data(self):
        self.label_layer_name.clear()
        self.label_filepath.clear()


    def clear_parameter_data(self):
        clear_layout(self.parameters_layout)


    def _on_export_clicked(self):
        EISMessageManager().show_message("Model history exporting not implemented yet!", "invalid")


    def _on_delete_clicked(self):
        reply = QMessageBox.question(
            self,
            "Confirm deletion",
            "Are you sure you want to delete the selected model history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            model = self.model_selection.currentText()
            new_index = min(self.model_selection.currentIndex(), self.model_selection.count() - 2)
            self.model_manager.remove_model_info(model)
            self.update_list_of_models(index=new_index)
            EISMessageManager().show_message(f"Model {model} deleted.", "success")


    def _on_delete_all_clicked(self):
        reply = QMessageBox.question(
            self,
            "Confirm deletion",
            "Are you sure you want to delete ALL model histories?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.model_manager.remove_model_info_all()
            self.update_list_of_models()
            EISMessageManager().show_message("All models deleted.", "success")
