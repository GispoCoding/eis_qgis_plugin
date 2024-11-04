from typing import Optional

from qgis.core import QgsApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)

from eis_qgis_plugin.eis_wizard.mineral_proxies.mineral_system import MineralProxy, MineralSystem, ProxyImportance
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.message_manager import EISMessageManager
from eis_qgis_plugin.utils.misc_utils import find_index_for_text_combobox

FORM_CLASS = load_ui("mineral_proxies/modify_custom_proxy.ui")

WORKFLOW_STEPS = ["Distance to features", "Distance to anomaly", "Interpolate"]


class EISWizardModifyProxy(QDialog, FORM_CLASS):

    def __init__(self, mineral_system: MineralSystem, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setupUi(self)

        self.modify_proxy_selection: QComboBox

        self.name: QLineEdit
        self.mineral_system_component: QComboBox
        self.category: QComboBox
        self.regional_scale_importance: QComboBox
        self.camp_scale_importance: QComboBox
        self.deposit_scale_importance: QComboBox

        self.workflow_steps_layout: QFormLayout
        self.workflow_step_1_label: QPushButton
        self.workflow_step_1: QComboBox
        self.remove_workflow_step_btn: QPushButton
        self.add_workflow_step_btn: QPushButton

        self.button_box: QDialogButtonBox

        self.mineral_system = mineral_system
        self.proxy = None

        # UI
        self.add_workflow_step_btn.setIcon(QIcon(QgsApplication.iconPath('symbologyAdd.svg')))
        self.remove_workflow_step_btn.setIcon(QIcon(QgsApplication.iconPath('symbologyRemove.svg')))

        # SIGNALS
        self.add_workflow_step_btn.clicked.connect(self.add_workflow_step)
        self.remove_workflow_step_btn.clicked.connect(self.remove_workflow_step)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.button(QDialogButtonBox.Reset).clicked.connect(self._on_reset)

        # MODIFY STUFF
        self.modify_proxy_selection.currentIndexChanged.connect(self._on_proxy_selection_changed)
        self.modify_proxy_selection.addItems(proxy.name for proxy in self.mineral_system.proxies)


    def _on_proxy_selection_changed(self, i: int):
        self.proxy = self.mineral_system.proxies[i]     
        self.configure_widgets_from_proxy(self.proxy)


    def configure_widgets_from_proxy(self, proxy: MineralProxy):
        self.name.setText(proxy.name)
        component_i = find_index_for_text_combobox(
            self.mineral_system_component, proxy.mineral_system_component
        )
        self.mineral_system_component.setCurrentIndex(component_i)
        category_i = find_index_for_text_combobox(
            self.category, proxy.category
        )
        self.category.setCurrentIndex(category_i)
        regional_scale_importance_i = find_index_for_text_combobox(
            self.regional_scale_importance, proxy.regional_scale_importance.description
        )
        self.regional_scale_importance.setCurrentIndex(regional_scale_importance_i)
        camp_scale_importance_i = find_index_for_text_combobox(
            self.camp_scale_importance, proxy.camp_scale_importance.description
        )
        self.camp_scale_importance.setCurrentIndex(camp_scale_importance_i)
        deposit_scale_importance_i = find_index_for_text_combobox(
            self.deposit_scale_importance, proxy.deposit_scale_importance.description
        )
        self.deposit_scale_importance.setCurrentIndex(deposit_scale_importance_i)

        # Reset workflow steps
        while self.workflow_steps_layout.rowCount() > 0:
            self.remove_workflow_step(remove_last_row=True)

        # Add workflow steps
        for step in proxy.workflow:
            self.add_workflow_step(step)


    def add_workflow_step(self, step_name: Optional[str] = None):
        row_i = self.workflow_steps_layout.rowCount()

        label = QLabel(f"Step {row_i + 1}")
        workflow_selection = QComboBox()
        workflow_selection.addItems(WORKFLOW_STEPS)
        self.workflow_steps_layout.addRow(label, workflow_selection)
        if step_name:
            step_name_str = step_name.replace("_", " ").capitalize()
            i = find_index_for_text_combobox(workflow_selection, step_name_str)
            workflow_selection.setCurrentIndex(i)


    def remove_workflow_step(self, remove_last_row: bool = False):
        rows = self.workflow_steps_layout.rowCount()
        if remove_last_row:
            limit = 0
        else:
            limit = 1
        if rows > limit:
            self.workflow_steps_layout.removeRow(rows-1)
            self.resize(1, 1)


    def _on_reset(self):
        if self.proxy:
            self.configure_widgets_from_proxy(self.proxy)


    def _on_accept(self):
        workflow_steps = []
        for i in range(self.workflow_steps_layout.count()):
            widget = self.workflow_steps_layout.itemAt(i).widget()
            if isinstance(widget, QComboBox):
                step_txt = widget.currentText().replace(" ", "_").lower()
                workflow_steps.append(step_txt)

        if self.name.text().strip() == "":
            print("Proxy needs a valid name!")
            return

        if self.proxy:
            self.proxy.name = self.name.text()
            self.proxy.mineral_system_component=self.mineral_system_component.currentText().lower()
            self.proxy.category=self.category.currentText().lower()
            self.proxy.workflow=workflow_steps
            self.proxy.regional_scale_importance=ProxyImportance.from_description(
                self.regional_scale_importance.currentText()
            )
            self.proxy.camp_scale_importance=ProxyImportance.from_description(
                self.camp_scale_importance.currentText()
            )
            self.proxy.deposit_scale_importance=ProxyImportance.from_description(
                self.deposit_scale_importance.currentText()
            )
            EISMessageManager().show_message(f"Modified proxy {self.proxy.name}.", "success")
            self.accept()
