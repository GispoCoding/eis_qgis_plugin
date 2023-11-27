from qgis.PyQt.QtWidgets import QDialog, QWidget, QLineEdit, QCheckBox, QPushButton
from qgis.core import QgsSettings

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

_SETTINGS_KEY = "eis_qgis_plugin/python_venv_path"
_DOCK_SETTING = "eis_qgis_plugin/dock_setting"

FORM_CLASS: QDialog = load_ui("wizard_settings.ui")


class EISWizardSettings(QWidget, FORM_CLASS):

    toolkit_venv_path: QLineEdit
    dock_wizard_selection: QCheckBox
    layer_group_selection: QCheckBox
    save_settings_btn: QPushButton

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.settings = QgsSettings()

        self.toolkit_venv_path.setText(self.get_toolkit_venv_path())
        self.dock_wizard_selection.setChecked(self.get_dock_wizard_selection())

        self.save_settings_btn.clicked.connect(self.save)

    def get_toolkit_venv_path(self):
        return self.settings.value(_SETTINGS_KEY, "")

    def set_toolkit_venv_path(self, path: str):
        self.settings.setValue(_SETTINGS_KEY, path)

    def get_dock_wizard_selection(self):
        return self.settings.value(_DOCK_SETTING, "") == "true"

    def set_dock_wizard_selection(self, value: bool):
        if value:
            self.settings.setValue(_DOCK_SETTING, "true")
        else:
            self.settings.setValue(_DOCK_SETTING, "")

    def save(self):
        self.set_toolkit_venv_path(self.toolkit_venv_path.text())
        self.set_dock_wizard_selection(self.dock_wizard_selection.isChecked())
