from qgis.core import QgsSettings

_ENV_KEY = "eis_qgis_plugin/python_env_path"


def get_python_env_path():
    settings = QgsSettings()
    return settings.value(_ENV_KEY, "")


def save_python_venv_path(path):
    settings = QgsSettings()
    settings.setValue(_ENV_KEY, path)
