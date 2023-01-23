import os

from qgis.gui import QgisInterface

from eis_wizard.qgis_plugin_tools.infrastructure.debugging import setup_debugpy  # noqa F401
from eis_wizard.qgis_plugin_tools.infrastructure.debugging import setup_ptvsd  # noqa F401
from eis_wizard.qgis_plugin_tools.infrastructure.debugging import setup_pydevd  # noqa F401

debugger = os.environ.get("QGIS_PLUGIN_USE_DEBUGGER", "").lower()
if debugger in {"debugpy", "ptvsd", "pydevd"}:
    locals()["setup_" + debugger]()


def classFactory(iface: QgisInterface):  # noqa N802
    from eis_wizard.plugin import Plugin

    return Plugin()
