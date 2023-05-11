from qgis.core import QgsSettings

_SETTINGS_KEY = "eis_qgis_plugin/python_venv_path"


def get_python_venv_path():
    settings = QgsSettings()
    return settings.value(_SETTINGS_KEY, "")


def save_python_venv_path(path):
    settings = QgsSettings()
    settings.setValue(_SETTINGS_KEY, path)
