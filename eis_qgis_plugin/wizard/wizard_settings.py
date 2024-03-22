from qgis.gui import QgsColorButton, QgsFileWidget
from qgis.PyQt.QtWidgets import QCheckBox, QComboBox, QDialog, QLabel, QLineEdit, QPushButton, QRadioButton, QWidget
from qgis.utils import iface

from eis_qgis_plugin.processing.eis_toolkit_invoker import EISToolkitInvoker
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.utils.settings_manager import EISSettingsManager

FORM_CLASS: QDialog = load_ui("wizard_settings.ui")


class EISWizardSettings(QWidget, FORM_CLASS):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # DECLARE TYPES
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

        self.dock_wizard_selection: QCheckBox
        self.layer_group_selection: QCheckBox
        self.categorical_palette_selection: QComboBox
        self.continuous_palette_selection: QComboBox
        self.default_color_selection: QgsColorButton

        self.save_settings_btn: QPushButton
        self.reset_settings_btn: QPushButton

        # Connect signals
        self.save_settings_btn.clicked.connect(self.save_settings)
        self.reset_settings_btn.clicked.connect(self.reset_settings_to_default)

        self.docker_selection.toggled.connect(self._on_environment_type_changed)
        self.check_for_toolkit_btn.clicked.connect(self._on_check_for_toolkit_btn_clicked)

        self.docker_image_name.textChanged.connect(self.reset_verification_labels)
        self.venv_directory.fileChanged.connect(self.reset_verification_labels)

        # Initialize
        self._on_environment_type_changed(self.docker_selection.isChecked())
        self.load_settings()  # Initialize UI from settings


    def initialize_toolkit_configuration(self):
        """Initialize toolkit"""
        self.docker_selection.toggled.connect(self._on_environment_type_changed)
        self.check_for_toolkit_btn.clicked.connect(self._on_check_for_toolkit_btn_clicked)

        self.docker_image_name.textChanged.connect(self.reset_verification_labels)
        self.venv_directory.fileChanged.connect(self.reset_verification_labels)


    def reset_verification_labels(self, text = None):
        """Reset verification label widgets."""
        self.environment_validity_label.setText("-")
        self.environment_validity_label.setStyleSheet("color: black;")

        self.toolkit_validity_label.setText("-")
        self.toolkit_validity_label.setStyleSheet("color: black;")


    def _on_environment_type_changed(self, docker_selected: bool):
        """Called when radio buttons controlling environment type selections are toggled."""
        if docker_selected:
            self.set_docker_selection()
        else:
            self.set_venv_selection()


    def set_docker_selection(self):
        """Set widgets to reflect active Docker selection in EIS Toolkit configuration."""
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


    def set_venv_selection(self):
        """Set widgets to reflect active venv selection in EIS Toolkit configuration."""
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


    def _on_check_for_toolkit_btn_clicked(self):        
        self.reset_verification_labels()

        toolkit_invoker = EISToolkitInvoker(
            self.env_type, self.venv_directory.filePath(), self.docker_path.filePath(), self.docker_image_name.text()
        )
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


    def load_settings(self):
        """Load settings and set selections accordingly."""
        self.venv_selection.setChecked(EISSettingsManager.get_environment_selection() == "venv")
        self.docker_selection.setChecked(EISSettingsManager.get_environment_selection() == "docker")
        self.venv_directory.setFilePath(EISSettingsManager.get_venv_directory())
        self.docker_path.setFilePath(EISSettingsManager.get_docker_path())
        self.docker_image_name.setText(EISSettingsManager.get_docker_image_name())
        self.docker_host_folder.setFilePath(EISSettingsManager.get_docker_host_folder())
        self.docker_temp_folder.setFilePath(EISSettingsManager.get_docker_temp_folder())
        self.dock_wizard_selection.setChecked(EISSettingsManager.get_dock_wizard_selection())
        self.default_color_selection.setColor(EISSettingsManager.get_default_color())
        self.categorical_palette_selection.setCurrentText(EISSettingsManager.get_default_categorical_palette())
        self.continuous_palette_selection.setCurrentText(EISSettingsManager.get_default_continuous_palette())
        self.layer_group_selection.setChecked(EISSettingsManager.get_layer_group_selection())


    def save_settings(self):
        """Save current selections."""
        EISSettingsManager.set_environment_selection(self.env_type)
        EISSettingsManager.set_venv_directory(self.venv_directory.filePath())
        EISSettingsManager.set_docker_path(self.docker_path.filePath())
        EISSettingsManager.set_docker_image_name(self.docker_image_name.text())
        EISSettingsManager.set_docker_host_folder(self.docker_host_folder.filePath())
        EISSettingsManager.set_docker_temp_folder(self.docker_temp_folder.filePath())
        EISSettingsManager.set_dock_wizard_selection(self.dock_wizard_selection.isChecked())
        EISSettingsManager.set_color_selection(self.default_color_selection.color())
        EISSettingsManager.set_categorical_palette_selection(self.categorical_palette_selection.currentText())
        EISSettingsManager.set_continuous_palette_selection(self.continuous_palette_selection.currentText())
        EISSettingsManager.set_layer_group_selection(self.layer_group_selection.isChecked())

        iface.messageBar().pushSuccess("Success:", "Saved EIS QGIS plugin settings.")


    def reset_settings_to_default(self):
        """Set selections to defaults. Does not save."""
        defaults = EISSettingsManager.DEFAULTS

        self.venv_selection.setChecked(defaults[EISSettingsManager.ENVIRONMENT_SELECTION_SETTING] == "venv")
        self.docker_selection.setChecked(defaults[EISSettingsManager.ENVIRONMENT_SELECTION_SETTING] == "docker")
        self.venv_directory.setFilePath(defaults[EISSettingsManager.VENV_DIRECTORY_SETTING])
        self.docker_path.setFilePath(defaults[EISSettingsManager.DOCKER_PATH_SETTING])
        self.docker_image_name.setText(defaults[EISSettingsManager.DOCKER_IMAGE_SETTING])
        self.docker_host_folder.setFilePath(defaults[EISSettingsManager.DOCKER_HOST_FOLDER])
        self.docker_temp_folder.setFilePath(defaults[EISSettingsManager.DOCKER_TEMP_FOLDER])
        self.dock_wizard_selection.setChecked(defaults[EISSettingsManager.DOCK_SETTING])
        self.default_color_selection.setColor(defaults[EISSettingsManager.COLOR_SETTING])
        self.categorical_palette_selection.setCurrentText(defaults[EISSettingsManager.CATEGORICAL_PALETTE_SETTING])
        self.continuous_palette_selection.setCurrentText(defaults[EISSettingsManager.CONTINUOUS_PALETTE_SETTING])
        self.layer_group_selection.setChecked(defaults[EISSettingsManager.LAYER_GROUP_SETTING])

        iface.messageBar().pushInfo("Info:", "EIS QGIS plugin settings reset.")
