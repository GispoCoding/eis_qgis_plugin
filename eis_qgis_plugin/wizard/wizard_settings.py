from qgis.core import QgsSettings
from qgis.gui import QgsColorButton
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QCheckBox, QComboBox, QDialog, QLineEdit, QPushButton, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

_VENV_PATH_SETTING = "eis_qgis_plugin/python_venv_path"
_DOCK_SETTING = "eis_qgis_plugin/dock_setting"
_LAYER_GROUP_SETTING = "eis_qgis_plugin/layer_group_setting"
_CATEGORICAL_PALETTE_SETTING = "eis_qgis_plugin/categorical_palette_setting"
_CONTINUOUS_PALETTE_SETTING = "eis_qgis_plugin/continuous_palette_setting"
_COLOR_SETTING = "eis_qgis_plugin/default_color_setting"

DEFAULTS = {
    _VENV_PATH_SETTING: "",
    _DOCK_SETTING: False,
    _LAYER_GROUP_SETTING: False,
    _CATEGORICAL_PALETTE_SETTING: "dark",
    _CONTINUOUS_PALETTE_SETTING: "viridis",
    _COLOR_SETTING: QColor(0, 45, 179)
}


FORM_CLASS: QDialog = load_ui("wizard_settings.ui")


class EISWizardSettings(QWidget, FORM_CLASS):

    toolkit_venv_path: QLineEdit
    dock_wizard_selection: QCheckBox
    layer_group_selection: QCheckBox
    categorical_palette_selection: QComboBox
    continuous_palette_selection: QComboBox
    default_color_selection: QgsColorButton

    save_settings_btn: QPushButton
    reset_settings_btn: QPushButton


    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.settings = QgsSettings()

        self.save_settings_btn.clicked.connect(self.save)
        self.reset_settings_btn.clicked.connect(self.reset_to_defaults)

        self.load()  # Initialize UI from settings

    # INDIVIDUAL GET MEHTODS
    def get_toolkit_venv_path(self):
        key = _VENV_PATH_SETTING
        return self.settings.value(key, "") if key else DEFAULTS[key]

    def get_dock_wizard_selection(self):
        key = _DOCK_SETTING
        return self.settings.value(key, "") == "true" if key else DEFAULTS[key]

    def get_default_color(self):
        key = _COLOR_SETTING
        return self.settings.value(key) if key else DEFAULTS[key]

    def get_default_categorical_palette(self):
        key = _CATEGORICAL_PALETTE_SETTING
        return self.settings.value(key) if key else DEFAULTS[key]

    def get_default_continuous_palette(self):
        key = _CONTINUOUS_PALETTE_SETTING
        return self.settings.value(key) if key else DEFAULTS[key]

    def get_layer_group_selection(self):
        key = _LAYER_GROUP_SETTING
        return self.settings.value(key) == "true" if key else DEFAULTS[key]

    # INDIVIDUAL SET METHODS
    def set_toolkit_venv_path(self):
        path = self.toolkit_venv_path.text()
        self.settings.setValue(_VENV_PATH_SETTING, path)

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
        self.toolkit_venv_path.setText(self.get_toolkit_venv_path())
        self.dock_wizard_selection.setChecked(self.get_dock_wizard_selection())
        self.default_color_selection.setColor(self.get_default_color())
        self.categorical_palette_selection.setCurrentText(self.get_default_categorical_palette())
        self.continuous_palette_selection.setCurrentText(self.get_default_continuous_palette())
        self.layer_group_selection.setChecked(self.get_layer_group_selection())

    def save(self):
        """Save current selections."""
        self.set_toolkit_venv_path()
        self.set_dock_wizard_selection()
        self.set_color_selection()
        self.set_categorical_palette_selection()
        self.set_continuous_palette_selection()
        self.set_layer_group_selection()

    def reset_to_defaults(self):
        """Set selections to defaults. Does not save."""
        self.toolkit_venv_path.setText(DEFAULTS[_VENV_PATH_SETTING])
        self.dock_wizard_selection.setChecked(DEFAULTS[_DOCK_SETTING])
        self.default_color_selection.setColor(DEFAULTS[_COLOR_SETTING])
        self.categorical_palette_selection.setCurrentText(DEFAULTS[_CATEGORICAL_PALETTE_SETTING])
        self.continuous_palette_selection.setCurrentText(DEFAULTS[_CONTINUOUS_PALETTE_SETTING])
        self.layer_group_selection.setChecked(DEFAULTS[_LAYER_GROUP_SETTING])
