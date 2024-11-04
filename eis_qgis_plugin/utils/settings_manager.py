import json
from typing import Optional

from qgis.core import (
    QgsColorRamp,
    QgsGradientColorRamp,
    QgsGradientStop,
    QgsProject,
    QgsRasterLayer,
    QgsSettings,
    QgsStyle,
)
from qgis.PyQt.QtGui import QColor

from eis_qgis_plugin.utils.message_manager import EISMessageManager


class ColorRampEncoder(json.JSONEncoder):
    def default(self, obj: QgsGradientColorRamp):
        if isinstance(obj, QColor):
            return obj.name()  # QColor to hex string
        elif isinstance(obj, QgsGradientStop):
            return {
                'offset': obj.offset,
                'color': obj.color.name()  # QColor to hex string
            }
        return json.JSONEncoder.default(self, obj)

    def decode(dct: dict):
        for key, value in dct.items():
            if isinstance(value, str) and value.startswith('#') and len(value) == 7:
                try:
                    dct[key] = QColor(value)  # Convert hex string back to QColor
                except ValueError:
                    pass
            elif key == "stops":
                try:
                    decoded_stops = []
                    for stop in value: 
                        offset = stop['offset']
                        color = QColor(stop['color'])  # Convert hex string back to QColor
                        decoded_stops.append(QgsGradientStop(offset, color))
                    dct[key] = decoded_stops
                except ValueError:
                    pass
        return dct


def default_ramp():
    ramp = QgsStyle().defaultStyle().colorRamp("Spectral")
    return ramp


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
    MINIMAL_MENU_SETTING = "eis_qgis_plugin/minimal_menu_setting"
    LAYER_GROUP_SETTING = "eis_qgis_plugin/layer_group_setting"
    CATEGORICAL_PALETTE_SETTING = "eis_qgis_plugin/categorical_palette_setting"
    CONTINUOUS_PALETTE_SETTING = "eis_qgis_plugin/continuous_palette_setting"
    RASTER_COLOR_RAMP_SETTING = "eis_qgis_plugin/raster_color_ramp_setting"
    COLOR_SETTING = "eis_qgis_plugin/default_color_setting"
    DEFAULT_BASE_RASTER = "eis_qgis_plugin/default_base_raster"

    DEFAULTS = {
        ENVIRONMENT_SELECTION_SETTING: "venv",
        DOCKER_PATH_SETTING: "",
        VENV_DIRECTORY_SETTING: "",
        DOCKER_IMAGE_SETTING: "",
        DOCKER_HOST_FOLDER: "",
        DOCKER_TEMP_FOLDER: "",
        DOCK_SETTING: "false",
        MINIMAL_MENU_SETTING: "false",
        LAYER_GROUP_SETTING: "false",
        CATEGORICAL_PALETTE_SETTING: "bright",
        CONTINUOUS_PALETTE_SETTING: "viridis",
        RASTER_COLOR_RAMP_SETTING: default_ramp(),
        COLOR_SETTING: QColor(72, 172, 50),
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
        return QgsSettings().value(key, self.DEFAULTS[key]).lower() == "true"

    @classmethod
    def get_minimal_menu_selection(self) -> bool:
        key = self.MINIMAL_MENU_SETTING
        return QgsSettings().value(key, self.DEFAULTS[key]).lower() == "true"

    @classmethod
    def get_raster_color_ramp(self) -> QgsColorRamp:
        key = self.RASTER_COLOR_RAMP_SETTING

        # Deserialize color ramp
        try:
            serialized_items = QgsSettings().value(key, self.DEFAULTS[key])
            ramp = QgsGradientColorRamp(**json.loads(serialized_items, object_hook=ColorRampEncoder.decode))
        
        # If error, reset
        except (TypeError, json.JSONDecodeError) as e:
            self.reset_color_ramp_selection()
            EISMessageManager().show_message(
                f"Failed to load default raster color ramp info. Color ramp setting reset. {e}",
                "error"
            )

            serialized_items = QgsSettings().value(key, self.DEFAULTS[key])
            ramp = QgsGradientColorRamp(**json.loads(serialized_items, object_hook=ColorRampEncoder.decode))

        return ramp

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
        return QgsSettings().value(key, self.DEFAULTS[key]).lower() == "true"

    @classmethod
    def get_default_base_raster(self) -> Optional[QgsRasterLayer]:
        key = self.DEFAULT_BASE_RASTER
        raster_id = QgsSettings().value(key, self.DEFAULTS[key])
        if raster_id:
            layer = QgsProject.instance().mapLayer(raster_id)
            if isinstance(layer, QgsRasterLayer) and layer.isValid():
                return layer
        return None


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
        QgsSettings().setValue(self.DOCK_SETTING, "true" if selection else "false")

    @classmethod
    def set_minimal_menu_selection(self, selection: bool):
        QgsSettings().setValue(self.MINIMAL_MENU_SETTING, "true" if selection else "false")

    @classmethod
    def set_raster_color_ramp(self, ramp: QgsGradientColorRamp):
        # Serialize color ramp
        items = {"color1": ramp.color1(), "color2": ramp.color2(), "discrete": ramp.isDiscrete(), "stops": ramp.stops()}
        encoded_ramp = json.dumps(items, cls=ColorRampEncoder)
        QgsSettings().setValue(self.RASTER_COLOR_RAMP_SETTING, encoded_ramp)

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
        QgsSettings().setValue(self.LAYER_GROUP_SETTING, "true" if selection else "false")

    @classmethod
    def set_default_base_raster(self, base_raster: Optional[QgsRasterLayer]):
        if base_raster:
            QgsSettings().setValue(self.DEFAULT_BASE_RASTER, base_raster.id())
        else:
            QgsSettings().setValue(self.DEFAULT_BASE_RASTER, self.DEFAULTS[self.DEFAULT_BASE_RASTER])


    # RESETS
    @classmethod
    def reset_environment_selection(self):
        QgsSettings().setValue(self.ENVIRONMENT_SELECTION_SETTING, self.DEFAULTS[self.ENVIRONMENT_SELECTION_SETTING])

    @classmethod
    def reset_venv_directory(self):
        QgsSettings().setValue(self.VENV_DIRECTORY_SETTING, self.DEFAULTS[self.VENV_DIRECTORY_SETTING])

    @classmethod
    def reset_docker_path(self):
       QgsSettings().setValue(self.DOCKER_PATH_SETTING, self.DEFAULTS[self.DOCKER_PATH_SETTING])

    @classmethod
    def reset_docker_image_name(self):
        QgsSettings().setValue(self.DOCKER_IMAGE_SETTING, self.DEFAULTS[self.DOCKER_IMAGE_SETTING])

    @classmethod
    def reset_docker_host_folder(self):
        QgsSettings().setValue(self.DOCKER_HOST_FOLDER, self.DEFAULTS[self.DOCKER_HOST_FOLDER])
    
    @classmethod
    def reset_docker_temp_folder(self):
        QgsSettings().setValue(self.DOCKER_TEMP_FOLDER, self.DEFAULTS[self.DOCKER_TEMP_FOLDER])
    
    @classmethod
    def reset_dock_wizard_selection(self):
        QgsSettings().setValue(self.DOCK_SETTING, self.DEFAULTS[self.DOCK_SETTING] == "true")

    @classmethod
    def reset_minimal_menu_selection(self):
        QgsSettings().setValue(self.MINIMAL_MENU_SETTING, self.DEFAULTS[self.MINIMAL_MENU_SETTING] == "true")

    @classmethod
    def reset_color_ramp_selection(self):
        self.set_raster_color_ramp(self.DEFAULTS[self.RASTER_COLOR_RAMP_SETTING])

    @classmethod
    def reset_color_selection(self):
        QgsSettings().setValue(self.COLOR_SETTING, self.DEFAULTS[self.COLOR_SETTING])
    
    @classmethod
    def reset_categorical_palette_selection(self):
        QgsSettings().setValue(self.CATEGORICAL_PALETTE_SETTING, self.DEFAULTS[self.CATEGORICAL_PALETTE_SETTING])
    
    @classmethod
    def reset_continuous_palette_selection(self):
        QgsSettings().setValue(self.CONTINUOUS_PALETTE_SETTING, self.DEFAULTS[self.CONTINUOUS_PALETTE_SETTING])
    
    @classmethod
    def reset_layer_group_selection(self):
        QgsSettings().setValue(self.LAYER_GROUP_SETTING, self.DEFAULTS[self.LAYER_GROUP_SETTING] == "true")

    @classmethod
    def reset_default_base_raster(self):
        QgsSettings().setValue(self.DEFAULT_BASE_RASTER, self.DEFAULTS[self.DEFAULT_BASE_RASTER])


    @classmethod
    def reset_all(self):
        self.reset_environment_selection()
        self.reset_venv_directory()
        self.reset_docker_path()
        self.reset_docker_image_name()
        self.reset_docker_host_folder()
        self.reset_docker_temp_folder()
        self.reset_dock_wizard_selection()
        self.reset_minimal_menu_selection()
        self.reset_color_ramp_selection()
        self.reset_color_selection()
        self.reset_categorical_palette_selection()
        self.reset_continuous_palette_selection()
        self.reset_layer_group_selection()
        self.reset_default_base_raster()
