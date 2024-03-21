from qgis.PyQt.QtWidgets import QComboBox, QDialog, QLineEdit, QPushButton, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.model_manager import ModelManager

FORM_CLASS: QDialog = load_ui("results/wizard_model_history.ui")


class EISWizardHistory(QWidget, FORM_CLASS):   

    def __init__(self, parent=None, model_manager: ModelManager = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.model_manager = model_manager

        # DECLARE TYPES
        self.model_selection: QComboBox
        self.model_name: QLineEdit
        self.model_file: QLineEdit

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
        self.update_list_of_models(0)


    def update_list_of_models(self, index: int = None):
        models = ModelManager.get_all_models()
        self.model_selection.clear()
        self.model_selection.addItems(models)
        if index is not None:
            self.model_selection.setCurrentIndex(index)


    def update_viewed_model(self, model_id: str):
        info = ModelManager.get_model_info(model_id)
        if info is None:
            self.model_name.clear()
            self.model_file.clear()
        else:
            self.model_name.setText(info["model_name"])
            self.model_file.setText(info["model_file"])


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