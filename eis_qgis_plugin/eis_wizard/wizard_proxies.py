import json
import os
from typing import Optional, Sequence

from qgis.PyQt.QtWidgets import (
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from eis_qgis_plugin.eis_wizard.mineral_proxies.mineral_system import MINERAL_SYSTEMS_DIR, MineralProxy, MineralSystem
from eis_qgis_plugin.eis_wizard.mineral_proxies.proxy_view import EISWizardProxyView
from eis_qgis_plugin.eis_wizard.mineral_proxies.workflows.distance_to_anomaly import EISWizardProxyDistanceToAnomaly
from eis_qgis_plugin.eis_wizard.mineral_proxies.workflows.distance_to_features import EISWizardProxyDistanceToFeatures
from eis_qgis_plugin.eis_wizard.mineral_proxies.workflows.interpolate import EISWizardProxyInterpolate


class EISWizardProxies(QWidget):

    WORKFLOW_WIDGETS = {
        "distance_to_features": EISWizardProxyDistanceToFeatures,
        "interpolate": EISWizardProxyInterpolate,
        "distance_to_anomaly": EISWizardProxyDistanceToAnomaly,
    }

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.mineral_systems = self.initialize_mineral_systems()

        # Init widgets
        self.proxy_view = EISWizardProxyView(proxy_manager=self, mineral_systems=self.mineral_systems)
        self.proxy_pages = QStackedWidget(self)
        self.proxy_pages.addWidget(self.proxy_view)

        layout = QVBoxLayout()
        layout.addWidget(self.proxy_pages)
        self.setLayout(layout)

        self.active_proxy_name: Optional[str] = None


    def initialize_mineral_systems(self) -> Sequence[MineralSystem]:
        mineral_systems = []
        # Find all JSON files in the folder dedicated to mineral system libraries
        for file_name in os.listdir(MINERAL_SYSTEMS_DIR):
            if file_name.endswith(".json"):
                mineral_system_dict = self._read_mineral_system_json(file_name)
                mineral_system = MineralSystem.new(mineral_system_dict)
                mineral_systems.append(mineral_system)
        return mineral_systems


    def _read_mineral_system_json(self, file_name) -> dict:
        fp = os.path.join(MINERAL_SYSTEMS_DIR, file_name)
        with open(fp, "r") as file:
            mineral_system_dict = json.loads(file.read())
        return mineral_system_dict



# ------------------------------


    def enter_proxy_processing(self, mineral_system_name: str, proxy: MineralProxy):  
        # Cleanup if changing proxy
        if self.active_proxy_name and self.active_proxy_name != proxy.name:
            self.delete_proxy_processing_pages()
        
        steps = len(proxy.workflow)
        if steps > 1:
            last_i = steps - 1
            for i, workflow_step_name in enumerate(proxy.workflow):
                widget_cls = self.WORKFLOW_WIDGETS[workflow_step_name]
                processing_page = widget_cls(
                    proxy_manager=self,
                    mineral_system=mineral_system_name,
                    category=proxy.category,
                    proxy_name=proxy.name,
                    mineral_system_component=proxy.mineral_system_component,
                    process_type="multi_step" if i != last_i else "multi_step_final"
                )
                self.proxy_pages.addWidget(processing_page)
        else:
            processing_page = self.WORKFLOW_WIDGETS[proxy.workflow[0]](
                proxy_manager=self,
                mineral_system=mineral_system_name,
                category=proxy.category,
                proxy_name=proxy.name,
                mineral_system_component=proxy.mineral_system_component,
                process_type="single_step"
            )
            self.proxy_pages.addWidget(processing_page)

        self.active_proxy_name = proxy.name
        self.proxy_pages.setCurrentIndex(1)     


    def delete_proxy_processing_pages(self):
        for i in reversed(range(self.proxy_pages.count())):
            if i == 0:
                return
            widget = self.proxy_pages.widget(i)
            self.proxy_pages.removeWidget(self.proxy_pages.widget(i))
            widget.setParent(None)