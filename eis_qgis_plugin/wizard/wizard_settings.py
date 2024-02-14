from qgis.core import QgsSettings
from qgis.gui import QgsColorButton, QgsFileWidget
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QCheckBox, QComboBox, QDialog, QLabel, QLineEdit, QPushButton, QRadioButton, QWidget

from eis_qgis_plugin.processing.eis_toolkit_invoker import EISToolkitInvoker
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

_ENVIRONMENT_SELECTION_SETTING = "eis_qgis_plugin/environment_selection"
_VENV_DIRECTORY_SETTING = "eis_qgis_plugin/venv_path"
_DOCKER_PATH_SETTING = "eis_qgis_plugin/docker_path"
_DOCKER_IMAGE_SETTING = "eis_qgis_plugin/docker_image_name"
_DOCKER_HOST_FOLDER = "eis_qgis_plugin/docker_host_folder"
_DOCKER_TEMP_FOLDER = "eis_qgis_plugin/docker_temp_folder"
_DOCK_SETTING = "eis_qgis_plugin/dock_setting"
_LAYER_GROUP_SETTING = "eis_qgis_plugin/layer_group_setting"
_CATEGORICAL_PALETTE_SETTING = "eis_qgis_plugin/categorical_palette_setting"
_CONTINUOUS_PALETTE_SETTING = "eis_qgis_plugin/continuous_palette_setting"
_COLOR_SETTING = "eis_qgis_plugin/default_color_setting"

DEFAULTS = {
    _ENVIRONMENT_SELECTION_SETTING: "venv",
    _DOCKER_PATH_SETTING: "",
    _VENV_DIRECTORY_SETTING: "",
    _DOCKER_IMAGE_SETTING: "",
    _DOCKER_HOST_FOLDER: "",
    _DOCKER_TEMP_FOLDER: "",
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
    
        self.dock_wizard_selection: QCheckBox
        self.layer_group_selection: QCheckBox
        self.categorical_palette_selection: QComboBox
        self.continuous_palette_selection: QComboBox
        self.default_color_selection: QgsColorButton

        self.save_settings_btn: QPushButton
        self.reset_settings_btn: QPushButton

        self.settings = QgsSettings()

        self.save_settings_btn.clicked.connect(self.save_settings)
        self.reset_settings_btn.clicked.connect(self.reset_settings_to_default)

        self.initialize_toolkit_configuration()
        self.load_settings()  # Initialize UI from settings


    def initialize_toolkit_configuration(self):
        self.venv_selection: QRadioButton
        self.venv_directory_label: QLabel
        self.venv_directory: QgsFileWidget

        self.docker_selection: QRadioButton
        self.docker_path_label: QLabel
        self.docker_path: QgsFileWidget
        self.docker_image_name_label: QLabel
        self.docker_image_name: QLineEdit
        self.docker_host_folder_label: QLabel
        self.docker_host_folder: QgsFileWidget
        self.docker_temp_folder_label: QLabel
        self.docker_temp_folder: QgsFileWidget

        self.toolkit_validity_label: QLabel
        self.environment_validity_label: QLabel

        self.check_for_toolkit_btn: QPushButton

        self.docker_selection.toggled.connect(self.environment_type_changed)
        self.check_for_toolkit_btn.clicked.connect(self.verify_environment_and_toolkit)

        self.docker_image_name.textChanged.connect(self.reset_verification_labels)
        self.venv_directory.fileChanged.connect(self.reset_verification_labels)
        self.environment_type_changed(self.docker_selection.isChecked())  # Additional initialize


    def reset_verification_labels(self, text = None):
        self.environment_validity_label.setText("-")
        self.environment_validity_label.setStyleSheet("color: black;")

        self.toolkit_validity_label.setText("-")
        self.toolkit_validity_label.setStyleSheet("color: black;")


    def environment_type_changed(self, docker_selected: bool):
        if docker_selected:
            self.env_type = "docker"

            self.docker_path.setEnabled(True)
            self.docker_path_label.setEnabled(True)
            self.docker_image_name.setEnabled(True)
            self.docker_image_name_label.setEnabled(True)
            self.docker_host_folder.setEnabled(True)
            self.docker_host_folder_label.setEnabled(True)
            self.docker_temp_folder.setEnabled(True)
            self.docker_temp_folder_label.setEnabled(True)

            self.venv_directory.setEnabled(False)
            self.venv_directory_label.setEnabled(False)
        else:
            self.env_type = "venv"

            self.docker_path.setEnabled(False)
            self.docker_path_label.setEnabled(False)
            self.docker_image_name.setEnabled(False)
            self.docker_image_name_label.setEnabled(False)
            self.docker_host_folder.setEnabled(False)
            self.docker_host_folder_label.setEnabled(False)
            self.docker_temp_folder.setEnabled(False)
            self.docker_temp_folder_label.setEnabled(False)

            self.venv_directory.setEnabled(True)
            self.venv_directory_label.setEnabled(True)


    def verify_environment_and_toolkit(self):
        venv_directory = self.venv_directory.filePath()
        docker_path = self.docker_path.filePath()
        image_name = self.docker_image_name.text()
        
        self.reset_verification_labels()
    
        toolkit_invoker = EISToolkitInvoker(self.env_type, venv_directory, docker_path, image_name)
        env_result, env_message = toolkit_invoker.verify_environment()
        self.environment_validity_label.setText(env_message)
        if env_result:
            self.environment_validity_label.setStyleSheet("color: green;")
            
            # Only try to verify toolkit installation if environment itself is OK
            toolkit_result, toolkit_message = toolkit_invoker.verify_toolkit()
            self.toolkit_validity_label.setText(toolkit_message)
            if toolkit_result:
                self.toolkit_validity_label.setStyleSheet("color: green;")
            else:
                self.toolkit_validity_label.setStyleSheet("color: red;")
        else:
            self.environment_validity_label.setStyleSheet("color: red;")


    # INDIVIDUAL GET MEHTODS
    def get_environment_selection(self):
        key = _ENVIRONMENT_SELECTION_SETTING
        return self.settings.value(key, DEFAULTS[key])

    def get_venv_directory(self):
        key = _VENV_DIRECTORY_SETTING
        return self.settings.value(key, DEFAULTS[key])
    
    def get_docker_path(self):
        key = _DOCKER_PATH_SETTING
        return self.settings.value(key, DEFAULTS[key])
    
    def get_docker_image_name(self):
        key = _DOCKER_IMAGE_SETTING
        return self.settings.value(key, DEFAULTS[key])
    
    def get_docker_host_folder(self):
        key = _DOCKER_HOST_FOLDER
        return self.settings.value(key, DEFAULTS[key])

    def get_docker_temp_folder(self):
        key = _DOCKER_TEMP_FOLDER
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
    def set_environment_selection(self):
        self.settings.setValue(_ENVIRONMENT_SELECTION_SETTING, self.env_type)

    def set_venv_directory(self):
        directory = self.venv_directory.filePath()
        self.settings.setValue(_VENV_DIRECTORY_SETTING, directory)

    def set_docker_path(self):
        path = self.docker_path.filePath()
        self.settings.setValue(_DOCKER_PATH_SETTING, path)

    def set_docker_image_name(self):
        image_name = self.docker_image_name.text()
        self.settings.setValue(_DOCKER_IMAGE_SETTING, image_name)

    def set_docker_host_folder(self):
        folder = self.docker_host_folder.filePath()
        self.settings.setValue(_DOCKER_HOST_FOLDER, folder)

    def set_docker_temp_folder(self):
        folder = self.docker_temp_folder.filePath()
        self.settings.setValue(_DOCKER_TEMP_FOLDER, folder)

    def set_dock_wizard_selection(self):
        selection = self.dock_wizard_selection.isChecked()
        self.settings.setValue(_DOCK_SETTING, "true" if selection else "")

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

    def load_settings(self):
        """Load settings and set selections accordingly."""
        self.venv_selection.setChecked(self.get_environment_selection() == "venv")
        self.docker_selection.setChecked(self.get_environment_selection() == "docker")
        self.venv_directory.setFilePath(self.get_venv_directory())
        self.docker_path.setFilePath(self.get_docker_path())
        self.docker_image_name.setText(self.get_docker_image_name())
        self.docker_host_folder.setFilePath(self.get_docker_host_folder())
        self.docker_temp_folder.setFilePath(self.get_docker_temp_folder())
        self.dock_wizard_selection.setChecked(self.get_dock_wizard_selection())
        self.default_color_selection.setColor(self.get_default_color())
        self.categorical_palette_selection.setCurrentText(self.get_default_categorical_palette())
        self.continuous_palette_selection.setCurrentText(self.get_default_continuous_palette())
        self.layer_group_selection.setChecked(self.get_layer_group_selection())

    def save_settings(self):
        """Save current selections."""
        self.set_environment_selection()
        self.set_venv_directory()
        self.set_docker_path()
        self.set_docker_image_name()
        self.set_docker_host_folder()
        self.set_docker_temp_folder()
        self.set_dock_wizard_selection()
        self.set_color_selection()
        self.set_categorical_palette_selection()
        self.set_continuous_palette_selection()
        self.set_layer_group_selection()

    def reset_settings_to_default(self):
        """Set selections to defaults. Does not save."""
        self.venv_selection.setChecked(DEFAULTS[_ENVIRONMENT_SELECTION_SETTING] == "venv")
        self.docker_selection.setChecked(DEFAULTS[_ENVIRONMENT_SELECTION_SETTING] == "docker")
        self.venv_directory.setFilePath(DEFAULTS[_VENV_DIRECTORY_SETTING])
        self.docker_path.setFilePath(DEFAULTS[_DOCKER_PATH_SETTING])
        self.docker_image_name.setText(DEFAULTS[_DOCKER_IMAGE_SETTING])
        self.docker_host_folder.setFilePath(DEFAULTS[_DOCKER_HOST_FOLDER])
        self.docker_temp_folder.setFilePath(DEFAULTS[_DOCKER_TEMP_FOLDER])
        self.dock_wizard_selection.setChecked(DEFAULTS[_DOCK_SETTING])
        self.default_color_selection.setColor(DEFAULTS[_COLOR_SETTING])
        self.categorical_palette_selection.setCurrentText(DEFAULTS[_CATEGORICAL_PALETTE_SETTING])
        self.continuous_palette_selection.setCurrentText(DEFAULTS[_CONTINUOUS_PALETTE_SETTING])
        self.layer_group_selection.setChecked(DEFAULTS[_LAYER_GROUP_SETTING])
