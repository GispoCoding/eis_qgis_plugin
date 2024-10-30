from typing import List, Optional

from qgis.PyQt.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QLabel, QLineEdit, QWidget

from eis_qgis_plugin.eis_wizard.mineral_proxies.mineral_system import MineralSystem
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.misc_utils import clear_form_layout

FORM_CLASS = load_ui("mineral_proxies/import_proxy.ui")


class EISWizardImportProxy(QDialog, FORM_CLASS):

    def __init__(self, mineral_systems: List[MineralSystem], parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setupUi(self)

        self.mineral_system_selection: QComboBox
        self.proxy_selection: QComboBox
        self.name: QLineEdit
        self.mineral_system_component: QLineEdit
        self.category: QLineEdit
        self.regional_scale_importance: QLineEdit
        self.camp_scale_importance: QLineEdit
        self.deposit_scale_importance: QLineEdit
        self.workflow_steps_layout: QFormLayout
        self.button_box: QDialogButtonBox

        self.proxy = None
        self.selected_mineral_system = None
        self.mineral_systems = mineral_systems
        self.mineral_system_selection.addItems(system.name for system in self.mineral_systems)

        self.mineral_system_selection.currentIndexChanged.connect(self._on_mineral_system_changed)
        self.proxy_selection.currentIndexChanged.connect(self._on_proxy_changed)
        self.button_box.accepted.connect(self._on_ok_clicked)

        self._on_mineral_system_changed(self.mineral_system_selection.currentIndex())


    def _on_mineral_system_changed(self, i: int):
        self.selected_mineral_system = self.mineral_systems[i]
        self.proxy_selection.clear()
        for proxy in self.selected_mineral_system.proxies:
            self.proxy_selection.addItem(proxy.name)


    def _on_proxy_changed(self, i: int):
        # Clear layout
        clear_form_layout(self.workflow_steps_layout)

        if len(self.selected_mineral_system.proxies) > 0:
            self.proxy = self.selected_mineral_system.proxies[i]
            self.name.setText(self.proxy.name)
            self.mineral_system_component.setText(self.proxy.mineral_system_component.capitalize())
            self.category.setText(self.proxy.category.capitalize())
            self.regional_scale_importance.setText(str(self.proxy.regional_scale_importance))
            self.camp_scale_importance.setText(str(self.proxy.camp_scale_importance))
            self.deposit_scale_importance.setText(str(self.proxy.deposit_scale_importance))

            # Workflow
            for i, step in enumerate(self.proxy.workflow):
                label = QLabel(f"Step {i+1}")
                step_widget = QLineEdit(step.replace("_", " ").capitalize())
                step_widget.setReadOnly(True)
                self.workflow_steps_layout.addRow(label, step_widget)

        # Clear if no proxies
        else:
            self.proxy = None
            self.name.clear()
            self.mineral_system_component.clear()
            self.category.clear()
            self.regional_scale_importance.clear()
            self.camp_scale_importance.clear()
            self.deposit_scale_importance.clear()


    def _on_ok_clicked(self):
        if self.proxy:
            self.accept()
        else:
            print("No proxy selected!")
