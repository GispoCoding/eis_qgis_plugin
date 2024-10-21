from typing import Optional

from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.mineral_proxies.mineral_system import MineralProxy, MineralSystem

FORM_CLASS = load_ui("mineral_proxies/delete_proxy.ui")


class EISWizardDeleteProxy(QDialog, FORM_CLASS):

    proxy_deleted = pyqtSignal(MineralProxy)

    def __init__(self, mineral_system: MineralSystem, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setupUi(self)
        self.delete_proxy_selection: QComboBox
        self.button_box: QDialogButtonBox

        self.mineral_system = mineral_system
        self.delete_proxy_selection.addItems(proxy.name for proxy in self.mineral_system.proxies)
        self.button_box.accepted.connect(self.delete_proxy)

    def delete_proxy(self) -> MineralProxy:
        i = self.delete_proxy_selection.currentIndex()
        proxy = self.mineral_system.proxies[i]
        if proxy.custom:
            self.mineral_system.proxies.pop(i)
            self.accept()
        else:
            print("Cannot delete non-custom proxy")
