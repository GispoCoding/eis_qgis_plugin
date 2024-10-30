from typing import List, Optional

from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QLineEdit,
    QWidget,
)

from eis_qgis_plugin.eis_wizard.mineral_proxies.mineral_system import MineralSystem
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS = load_ui("mineral_proxies/new_mineral_system.ui")


class EISWizardNewMineralSystem(QDialog, FORM_CLASS):

    def __init__(self, mineral_systems: List[MineralSystem], parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setupUi(self)

        self.name: QLineEdit
        self.base_mineral_system: QComboBox
        self.button_box: QDialogButtonBox

        self.button_box.accepted.connect(self._on_accept)

        self.mineral_systems = mineral_systems
        for mineral_system in self.mineral_systems:
            self.base_mineral_system.addItem(mineral_system.name)

        self.new_mineral_system = None


    def _on_accept(self):
        base_proxies = []
        i = self.base_mineral_system.currentIndex()
        if i > 0:
            # -1 because combobox has "-" as first item
            base_proxies = self.mineral_systems[i-1].proxies

        self.new_mineral_system = MineralSystem(
            name=self.name.text(),
            custom=True,
            proxies=base_proxies
        )
        self.accept()
