from typing import Optional

from qgis.core import QgsMapLayer, QgsSettings
from qgis.PyQt.QtGui import QColor


class EISSettingsManager:
    """
    A centralized interface for accessing and modifying settings of EIS QGIS Plugin.
    
    A static class that does not need instantiation, i.e. it should be used like this: \n
    `env_selection = EISSettingsManager.get_environment_selection()`
    
    Settings are saved to QGIS project.
    """

    ENVIRONMENT_SELECTION_SETTING = "eis_qgis_plugin/environment_selection"
    VENV_DIRECTORY_SETTING = "eis_qgis_plugin/venv_path"
    DOCKER_PATH_SETTING = "eis_qgis_plugin/docker_path"
    DOCKER_IMAGE_SETTING = "eis_qgis_plugin/docker_image_name"
    DOCKER_HOST_FOLDER = "eis_qgis_plugin/docker_host_folder"
    DOCKER_TEMP_FOLDER = "eis_qgis_plugin/docker_temp_folder"
    DOCK_SETTING = "eis_qgis_plugin/dock_setting"
    LAYER_GROUP_SETTING = "eis_qgis_plugin/layer_group_setting"
    CATEGORICAL_PALETTE_SETTING = "eis_qgis_plugin/categorical_palette_setting"
    CONTINUOUS_PALETTE_SETTING = "eis_qgis_plugin/continuous_palette_setting"
    COLOR_SETTING = "eis_qgis_plugin/default_color_setting"
    DEFAULT_BASE_RASTER = "eis_qgis_plugin/default_base_raster"

    DEFAULTS = {
        ENVIRONMENT_SELECTION_SETTING: "venv",
        DOCKER_PATH_SETTING: "",
        VENV_DIRECTORY_SETTING: "",
        DOCKER_IMAGE_SETTING: "",
        DOCKER_HOST_FOLDER: "",
        DOCKER_TEMP_FOLDER: "",
        DOCK_SETTING: False,
        LAYER_GROUP_SETTING: False,
        CATEGORICAL_PALETTE_SETTING: "dark",
        CONTINUOUS_PALETTE_SETTING: "viridis",
        COLOR_SETTING: QColor(0, 45, 179),
        DEFAULT_BASE_RASTER: None
    }

    # GETTERS
    @classmethod
    def get_environment_selection(self) -> str:
        key = self.ENVIRONMENT_SELECTION_SETTING
        return QgsSettings().value(key, self.DEFAULTS[key])

    @classmethod
    def get_venv_directory(self) -> str:
        key = self.VENV_DIRECTORY_SETTING
        return QgsSettings().value(key, self.DEFAULTS[key])

    @classmethod
    def get_docker_path(self) -> str:
        key = self.DOCKER_PATH_SETTING
        return QgsSettings().value(key, self.DEFAULTS[key])
    
    @classmethod
    def get_docker_image_name(self) -> str:
        key = self.DOCKER_IMAGE_SETTING
        return QgsSettings().value(key, self.DEFAULTS[key])
    
    @classmethod
    def get_docker_host_folder(self) -> str:
        key = self.DOCKER_HOST_FOLDER
        return QgsSettings().value(key, self.DEFAULTS[key])

    @classmethod
    def get_docker_temp_folder(self) -> str:
        key = self.DOCKER_TEMP_FOLDER
        return QgsSettings().value(key, self.DEFAULTS[key])

    @classmethod
    def get_dock_wizard_selection(self) -> bool:
        key = self.DOCK_SETTING
        return QgsSettings().value(key, self.DEFAULTS[key])

    @classmethod
    def get_default_color(self) -> QColor:
        key = self.COLOR_SETTING
        return QgsSettings().value(key, self.DEFAULTS[key])

    @classmethod
    def get_default_categorical_palette(self) -> str:
        key = self.CATEGORICAL_PALETTE_SETTING
        return QgsSettings().value(key, self.DEFAULTS[key])

    @classmethod
    def get_default_continuous_palette(self) -> str:
        key = self.CONTINUOUS_PALETTE_SETTING
        return QgsSettings().value(key, self.DEFAULTS[key])

    @classmethod
    def get_layer_group_selection(self) -> bool:
        key = self.LAYER_GROUP_SETTING
        return QgsSettings().value(key, self.DEFAULTS[key])

    @classmethod
    def get_default_base_raster(self) -> Optional[QgsMapLayer]:
        key = self.DEFAULT_BASE_RASTER
        return QgsSettings().value(key, self.DEFAULTS[key])


    # SETTERS
    @classmethod
    def set_environment_selection(self, env_type: str):
        QgsSettings().setValue(self.ENVIRONMENT_SELECTION_SETTING, env_type)

    @classmethod
    def set_venv_directory(self, directory_path: str):
        QgsSettings().setValue(self.VENV_DIRECTORY_SETTING, directory_path)

    @classmethod
    def set_docker_path(self, docker_path: str):
       QgsSettings().setValue(self.DOCKER_PATH_SETTING, docker_path)

    @classmethod
    def set_docker_image_name(self, image_name: str):
        QgsSettings().setValue(self.DOCKER_IMAGE_SETTING, image_name)

    @classmethod
    def set_docker_host_folder(self, folder_path: str):
        QgsSettings().setValue(self.DOCKER_HOST_FOLDER, folder_path)
    
    @classmethod
    def set_docker_temp_folder(self, folder_path: str):
        QgsSettings().setValue(self.DOCKER_TEMP_FOLDER, folder_path)
    
    @classmethod
    def set_dock_wizard_selection(self, selection: bool):
        QgsSettings().setValue(self.DOCK_SETTING, selection)
    
    @classmethod
    def set_color_selection(self, color: QColor):
        QgsSettings().setValue(self.COLOR_SETTING, color)
    
    @classmethod
    def set_categorical_palette_selection(self, palette: str):
        QgsSettings().setValue(self.CATEGORICAL_PALETTE_SETTING, palette)
    
    @classmethod
    def set_continuous_palette_selection(self, palette: str):
        QgsSettings().setValue(self.CONTINUOUS_PALETTE_SETTING, palette)
    
    @classmethod
    def set_layer_group_selection(self, selection: bool):
        QgsSettings().setValue(self.LAYER_GROUP_SETTING, selection)

    @classmethod
    def set_default_base_raster(self, base_raster: Optional[QgsMapLayer]):
        QgsSettings().setValue(self.DEFAULT_BASE_RASTER, base_raster)
