from typing import Optional

from qgis.PyQt.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QWidget

from eis_qgis_plugin.eis_wizard.mineral_proxies.mineral_system import MineralProxy, MineralSystem
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.message_manager import EISMessageManager

FORM_CLASS = load_ui("mineral_proxies/delete_proxy.ui")


class EISWizardDeleteProxy(QDialog, FORM_CLASS):

    def __init__(self, mineral_system: MineralSystem, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setupUi(self)
        self.delete_proxy_selection: QComboBox
        self.button_box: QDialogButtonBox

        self.mineral_system = mineral_system
        self.delete_proxy_selection.addItems(proxy.name for proxy in self.mineral_system.proxies)
        self.button_box.accepted.connect(self.delete_proxy)

    def delete_proxy(self) -> MineralProxy:
        if len(self.mineral_system.proxies) > 0:
            i = self.delete_proxy_selection.currentIndex()
            proxy = self.mineral_system.proxies.pop(i)
            EISMessageManager().show_message(
                f"Removed proxy {proxy.name} from mineral system {self.mineral_system.name}.", "success"
            )
            self.accept()
