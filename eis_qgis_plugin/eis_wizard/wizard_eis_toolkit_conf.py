
from qgis.core import QgsApplication
from qgis.gui import QgsFileWidget
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QRadioButton,
    QStackedWidget,
    QWidget,
)
from qgis.utils import iface

from eis_qgis_plugin.environment.eis_toolkit_invoker import EISToolkitInvoker
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.settings_manager import EISSettingsManager

FORM_CLASS: QDialog = load_ui("wizard_toolkit_conf.ui")


CONF_BOX_DOCKER_HEIGHT = 136
CONF_BOX_VENV_HEIGHT = 49


class EISWizardToolkitConfiguration(QWidget, FORM_CLASS):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # DECLARE TYPES
        self.venv_selection: QRadioButton
        self.venv_directory_label: QLabel
        self.venv_directory: QgsFileWidget
        self.conf_stack: QStackedWidget

        self.docker_selection: QRadioButton
        self.docker_path_label: QLabel
        self.docker_path: QgsFileWidget
        self.docker_image_name_label: QLabel
        self.docker_image_name: QLineEdit
        self.docker_host_folder_label: QLabel
        self.docker_host_folder: QgsFileWidget
        self.docker_temp_folder_label: QLabel
        self.docker_temp_folder: QgsFileWidget

        self.environment_status_line: QLineEdit
        self.python_version_line: QLineEdit
        self.eis_toolkit_status_line: QLineEdit
        
        self.environment_button_box: QDialogButtonBox
        self.toolkit_conf_button_box: QDialogButtonBox

        # Initialize & connect signals
        self.venv_directory_label.setToolTip(
            "Path to Python virtual environment with EIS Toolkit installed in it."
        )

        self.toolkit_conf_button_box.button(QDialogButtonBox.Save).clicked.connect(self.save_settings)
        self.docker_selection.toggled.connect(self._on_environment_type_changed)

        self.verify_env_btn = self.environment_button_box.addButton(
            "Verify environment status", QDialogButtonBox.ActionRole
        )
        self.verify_env_btn.setIcon(QIcon(QgsApplication.getThemeIcon("mActionRefresh.svg")))
        self.verify_env_btn.clicked.connect(self._on_verify_env_btn_clicked)

        # self.create_venv_btn = self.venv_conf_button_box.addButton(
        #     "Create new venv and install EIS Toolkit", QDialogButtonBox.ActionRole
        # )
        # self.create_venv_btn.setIcon(QIcon(os.path.join(PLUGIN_PATH, "resources/icons/python_add_icon.png")))
        # self.create_venv_btn.clicked.connect(self.create_venv)
    
        self.upgrade_btn = self.environment_button_box.addButton(
            "Upgrade EIS Toolkit", QDialogButtonBox.ActionRole
        )
        self.upgrade_btn.setIcon(QIcon(QgsApplication.getThemeIcon("mActionStart.svg")))
        self.upgrade_btn.clicked.connect(self.upgrade_eis_toolkit)

        self.docker_image_name.textChanged.connect(self.reset_verification_labels)
        self.venv_directory.fileChanged.connect(self.reset_verification_labels)

        self._on_environment_type_changed(self.docker_selection.isChecked())
        self.load_settings()  # Initialize UI from settings


    def reset_verification_labels(self, text = None):
        """Reset verification widgets."""
        self.environment_status_line.clear()
        self.python_version_line.clear()
        self.eis_toolkit_status_line.clear()

        # self.environment_validity_label.setStyleSheet("color: black;")
        # self.toolkit_validity_label.setStyleSheet("color: black;")


    def _on_environment_type_changed(self, docker_selected: bool):
        """Called when radio buttons controlling environment type selections are toggled."""
        if docker_selected:
            self.conf_stack.setCurrentIndex(1)
            self.set_docker_selection()
            self.conf_stack.setMaximumHeight(16777215)  # Max height
        else:
            self.conf_stack.setCurrentIndex(0)
            self.set_venv_selection()
            self.conf_stack.setMaximumHeight(CONF_BOX_VENV_HEIGHT)


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


    def upgrade_eis_toolkit(self):
        reply = QMessageBox.question(
            self,
            "Confirm EIS Toolkit upgrade",
            "Do you want to upgrade EIS Toolkit to its latest version (in PyPI) in the selected environment?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            toolkit_invoker = EISToolkitInvoker(
                self.env_type,
                self.venv_directory.filePath(),
                self.docker_path.filePath(),
                self.docker_image_name.text()
            )
            env_result, env_message = toolkit_invoker.upgrade_toolkit()
            if env_result:
                iface.messageBar().pushSuccess("Success: ", env_message)
            else:
                iface.messageBar().pushCritical("Error: ", env_message)


    # def create_venv(self):
    #     dlg = EISVenvCreator(self)
    #     if dlg.exec():
    #         print("Finished installing EIS Toolkit")


    def _on_verify_env_btn_clicked(self):        
        self.reset_verification_labels()

        toolkit_invoker = EISToolkitInvoker(
            self.env_type, self.venv_directory.filePath(), self.docker_path.filePath(), self.docker_image_name.text()
        )
        env_result, env_message = toolkit_invoker.verify_environment()
        self.environment_status_line.setText(env_message)
        if env_result:
            self.environment_status_line.setStyleSheet("color: green;")
            
            # Only try to verify toolkit installation if environment itself is OK
            toolkit_result, toolkit_message = toolkit_invoker.verify_toolkit()
            self.eis_toolkit_status_line.setText(toolkit_message)
            if toolkit_result:
                self.eis_toolkit_status_line.setStyleSheet("color: green;")
            else:
                self.eis_toolkit_status_line.setStyleSheet("color: red;")
        else:
            self.environment_status_line.setStyleSheet("color: red;")


    def load_settings(self):
        """Load settings and set selections accordingly."""
        self.venv_selection.setChecked(EISSettingsManager.get_environment_selection() == "venv")
        self.docker_selection.setChecked(EISSettingsManager.get_environment_selection() == "docker")
        self.venv_directory.setFilePath(EISSettingsManager.get_venv_directory())
        self.docker_path.setFilePath(EISSettingsManager.get_docker_path())
        self.docker_image_name.setText(EISSettingsManager.get_docker_image_name())
        self.docker_host_folder.setFilePath(EISSettingsManager.get_docker_host_folder())
        self.docker_temp_folder.setFilePath(EISSettingsManager.get_docker_temp_folder())


    def save_settings(self):
        """Save current selections."""
        EISSettingsManager.set_environment_selection(self.env_type)
        EISSettingsManager.set_venv_directory(self.venv_directory.filePath())
        EISSettingsManager.set_docker_path(self.docker_path.filePath())
        EISSettingsManager.set_docker_image_name(self.docker_image_name.text())
        EISSettingsManager.set_docker_host_folder(self.docker_host_folder.filePath())
        EISSettingsManager.set_docker_temp_folder(self.docker_temp_folder.filePath())
        
        iface.messageBar().pushSuccess("Success: ", "Saved EIS Toolkit configuration.")
