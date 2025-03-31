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

from eis_qgis_plugin.eis_wizard.mineral_proxies.mineral_system import MineralProxy, ProxyImportance
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS = load_ui("mineral_proxies/define_custom_proxy.ui")

WORKFLOW_STEPS = [
    "Distance to features",
    "Distance to anomaly",
    "Interpolate",
    "Binarize",
    "Proximity to anomaly",
    "Proximity to features",
    "Vector density"
]


class EISWizardDefineProxy(QDialog, FORM_CLASS):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setupUi(self)

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

        # UI
        self.add_workflow_step_btn.setIcon(QIcon(QgsApplication.iconPath('symbologyAdd.svg')))
        self.remove_workflow_step_btn.setIcon(QIcon(QgsApplication.iconPath('symbologyRemove.svg')))

        # SIGNALS
        self.add_workflow_step_btn.clicked.connect(self.add_workflow_step)
        self.remove_workflow_step_btn.clicked.connect(self.remove_workflow_step)

        self.button_box.accepted.connect(self._on_accept)

        self.proxy = None
        self.add_workflow_step()


    def add_workflow_step(self):
        row_i = self.workflow_steps_layout.rowCount()

        label = QLabel(f"Step {row_i + 1}")
        workflow_selection = QComboBox()
        workflow_selection.addItems(WORKFLOW_STEPS)
        self.workflow_steps_layout.addRow(label, workflow_selection)


    def remove_workflow_step(self):
        rows = self.workflow_steps_layout.rowCount()
        if rows > 1:
            self.workflow_steps_layout.removeRow(rows-1)
            self.resize(1, 1)


    def _on_accept(self):
        workflow_steps = []
        for i in range(self.workflow_steps_layout.count()):
            widget = self.workflow_steps_layout.itemAt(i).widget()
            if isinstance(widget, QComboBox):
                step_txt = widget.currentText().replace(" ", "_").lower()
                workflow_steps.append(step_txt)

        if self.name.text().strip() != "":
            self.proxy = MineralProxy(
                name=self.name.text(),
                custom=True,
                mineral_system_component=self.mineral_system_component.currentText().lower(),
                category=self.category.currentText().lower(),
                workflow=workflow_steps,
                regional_scale_importance=ProxyImportance.from_description(
                    self.regional_scale_importance.currentText()
                ),
                camp_scale_importance=ProxyImportance.from_description(
                    self.camp_scale_importance.currentText()
                ),
                deposit_scale_importance=ProxyImportance.from_description(
                    self.deposit_scale_importance.currentText()
                ),
            )
            self.accept()
        else:
            print("Could not create new proxy, inputs wrong")
