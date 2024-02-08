import os

from qgis.core import QgsSettings
from qgis.gui import QgsColorButton, QgsFileWidget
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QCheckBox, QComboBox, QDialog, QLabel, QPushButton, QWidget

from eis_qgis_plugin.processing.eis_toolkit_invoker import EISToolkitInvoker
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

_ENV_PATH_SETTING = "eis_qgis_plugin/python_env_path"
_DOCK_SETTING = "eis_qgis_plugin/dock_setting"
_LAYER_GROUP_SETTING = "eis_qgis_plugin/layer_group_setting"
_CATEGORICAL_PALETTE_SETTING = "eis_qgis_plugin/categorical_palette_setting"
_CONTINUOUS_PALETTE_SETTING = "eis_qgis_plugin/continuous_palette_setting"
_COLOR_SETTING = "eis_qgis_plugin/default_color_setting"

DEFAULTS = {
    _ENV_PATH_SETTING: "",
    _DOCK_SETTING: False,
    _LAYER_GROUP_SETTING: False,
    _CATEGORICAL_PALETTE_SETTING: "dark",
    _CONTINUOUS_PALETTE_SETTING: "viridis",
    _COLOR_SETTING: QColor(0, 45, 179)
}


FORM_CLASS: QDialog = load_ui("wizard_settings.ui")


class EISWizardSettings(QWidget, FORM_CLASS):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.toolkit_env_path: QgsFileWidget
        self.dock_wizard_selection: QCheckBox
        self.layer_group_selection: QCheckBox
        self.categorical_palette_selection: QComboBox
        self.continuous_palette_selection: QComboBox
        self.default_color_selection: QgsColorButton

        self.save_settings_btn: QPushButton
        self.reset_settings_btn: QPushButton

        self.env_toolkit_validity_label: QLabel
        self.env_directory_validity_label: QLabel
        self.check_for_toolkit_btn: QPushButton

        self.settings = QgsSettings()

        self.save_settings_btn.clicked.connect(self.save)
        self.reset_settings_btn.clicked.connect(self.reset_to_defaults)
        self.check_for_toolkit_btn.clicked.connect(self.check_for_eis_toolkit)
        self.toolkit_env_path.fileChanged.connect(self.check_for_python_executable)

        self.load()  # Initialize UI from settings


    def check_for_eis_toolkit(self) -> bool:
        """
        Checks if the selected Python environment has EIS Toolkit correctly installed.
        
        Updates a label to show whether the selected environment has EIS Toolkit installed.
        """
        env_path = self.toolkit_env_path.filePath()
        if self.check_for_python_executable(env_path) is False:
            self.env_toolkit_validity_label.setText("Invalid: The environment is not correctly configured.")
            self.env_toolkit_validity_label.setStyleSheet("color: orange;")
            return False

        toolkit_invoker = EISToolkitInvoker(env_path)
        result, message = toolkit_invoker.check_environment_validity()

        self.env_toolkit_validity_label.setText(message)
        self.env_toolkit_validity_label.setStyleSheet("color: green;" if result else "color: red;")
        
        return result
    
    def check_for_python_executable(self, env_path: str) -> bool:
        """
        Checks if a Python executable is found in the selected directory (i.e. if it is a Python env).
        
        Updates a label to show whether the selected directory is a valid Python environment directory.
        """
        self.env_toolkit_validity_label.setText("-")
        self.env_toolkit_validity_label.setStyleSheet("color: black;")

        if os.name == "nt":
            python_exe = "Scripts/python.exe"
        else:
            python_exe = "bin/python"

        if env_path == "":
            self.env_directory_validity_label.setText("-")
            self.env_directory_validity_label.setStyleSheet("color: black;")
            return False

        exe_path = os.path.join(env_path, python_exe)
        if os.path.exists(exe_path):
            self.env_directory_validity_label.setText("Valid: Python executable found.")
            self.env_directory_validity_label.setStyleSheet("color: green;")
            return True
        else:
            self.env_directory_validity_label.setText("Invalid: No Python executable found.")
            self.env_directory_validity_label.setStyleSheet("color: red;")
            return False


    # INDIVIDUAL GET MEHTODS
    def get_toolkit_env_path(self):
        key = _ENV_PATH_SETTING
        return self.settings.value(key, DEFAULTS[key])

    def get_dock_wizard_selection(self):
        key = _DOCK_SETTING
        return self.settings.value(key, "") == "true" if key else DEFAULTS[key]

    def get_default_color(self):
        key = _COLOR_SETTING
        return self.settings.value(key, DEFAULTS[key])

    def get_default_categorical_palette(self):
        key = _CATEGORICAL_PALETTE_SETTING
        return self.settings.value(key, DEFAULTS[key])

    def get_default_continuous_palette(self):
        key = _CONTINUOUS_PALETTE_SETTING
        return self.settings.value(key, DEFAULTS[key])

    def get_layer_group_selection(self):
        key = _LAYER_GROUP_SETTING
        return self.settings.value(key) == "true" if key else DEFAULTS[key]

    # INDIVIDUAL SET METHODS
    def set_toolkit_env_path(self):
        path = self.toolkit_env_path.filePath()
        self.settings.setValue(_ENV_PATH_SETTING, path)

    def set_dock_wizard_selection(self):
        value = self.dock_wizard_selection.isChecked()
        self.settings.setValue(_DOCK_SETTING, "true" if value else "")

    def set_color_selection(self):
        color = self.default_color_selection.color()
        self.settings.setValue(_COLOR_SETTING, color)

    def set_categorical_palette_selection(self):
        palette = self.categorical_palette_selection.currentText()
        self.settings.setValue(_CATEGORICAL_PALETTE_SETTING, palette)

    def set_continuous_palette_selection(self):
        palette = self.continuous_palette_selection.currentText()
        self.settings.setValue(_CONTINUOUS_PALETTE_SETTING, palette)

    def set_layer_group_selection(self):
        value = self.layer_group_selection.isChecked()
        self.settings.setValue(_LAYER_GROUP_SETTING, "true" if value else "")

    def load(self):
        """Load settings and set selections accordingly."""
        self.toolkit_env_path.setFilePath(self.get_toolkit_env_path())
        self.dock_wizard_selection.setChecked(self.get_dock_wizard_selection())
        self.default_color_selection.setColor(self.get_default_color())
        self.categorical_palette_selection.setCurrentText(self.get_default_categorical_palette())
        self.continuous_palette_selection.setCurrentText(self.get_default_continuous_palette())
        self.layer_group_selection.setChecked(self.get_layer_group_selection())

    def save(self):
        """Save current selections."""
        self.set_toolkit_env_path()
        self.set_dock_wizard_selection()
        self.set_color_selection()
        self.set_categorical_palette_selection()
        self.set_continuous_palette_selection()
        self.set_layer_group_selection()

    def reset_to_defaults(self):
        """Set selections to defaults. Does not save."""
        self.toolkit_env_path.setFilePath(DEFAULTS[_ENV_PATH_SETTING])
        self.dock_wizard_selection.setChecked(DEFAULTS[_DOCK_SETTING])
        self.default_color_selection.setColor(DEFAULTS[_COLOR_SETTING])
        self.categorical_palette_selection.setCurrentText(DEFAULTS[_CATEGORICAL_PALETTE_SETTING])
        self.continuous_palette_selection.setCurrentText(DEFAULTS[_CONTINUOUS_PALETTE_SETTING])
        self.layer_group_selection.setChecked(DEFAULTS[_LAYER_GROUP_SETTING])
