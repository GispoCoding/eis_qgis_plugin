from typing import Optional

from qgis.PyQt.QtWidgets import (
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from eis_qgis_plugin.wizard.mineral_proxies.proxy_view import EISWizardProxyView
from eis_qgis_plugin.wizard.mineral_proxies.workflows.distance_to_anomaly import EISWizardProxyDistanceToAnomaly
from eis_qgis_plugin.wizard.mineral_proxies.workflows.distance_to_features import EISWizardProxyDistanceToFeatures
from eis_qgis_plugin.wizard.mineral_proxies.workflows.interpolate import EISWizardProxyInterpolate


class EISWizardProxies(QWidget):

    WORKFLOW_MAP = {
        1: EISWizardProxyDistanceToFeatures,
        2: EISWizardProxyInterpolate,
        3: EISWizardProxyDistanceToAnomaly,
        4: [EISWizardProxyInterpolate, EISWizardProxyDistanceToAnomaly]
    }

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.proxy_view = EISWizardProxyView(proxy_manager=self)
        self.proxy_pages = QStackedWidget(self)
        self.proxy_pages.addWidget(self.proxy_view)

        layout = QVBoxLayout()
        layout.addWidget(self.proxy_pages)
        self.setLayout(layout)

        self.active_proxy_name: Optional[str] = None


    def enter_proxy_processing(
        self,mineral_system: str,
        category: str,
        proxy_name: str,
        workflow: int,
        mineral_system_component: str
    ):  
        # Cleanup if changing proxy
        if self.active_proxy_name and self.active_proxy_name != proxy_name:
            self.delete_proxy_processing_pages()

        workflow_classes = self.WORKFLOW_MAP[workflow]
        if isinstance(workflow_classes, list):
            last_i = len(workflow_classes) - 1
            for i, cls in enumerate(workflow_classes):
                processing_page = cls(
                    proxy_manager=self,
                    mineral_system=mineral_system,
                    category=category,
                    proxy_name=proxy_name,
                    mineral_system_component=mineral_system_component,
                    process_type="multi_step" if i != last_i else "multi_step_final"
                )
                self.proxy_pages.addWidget(processing_page)
        else:
            processing_page = self.WORKFLOW_MAP[workflow](
                proxy_manager=self,
                mineral_system=mineral_system,
                category=category,
                proxy_name=proxy_name,
                mineral_system_component=mineral_system_component,
                process_type="single_step"
            )
            self.proxy_pages.addWidget(processing_page)

        self.active_proxy_name = proxy_name
        self.proxy_pages.setCurrentIndex(1)     


    def delete_proxy_processing_pages(self):
        for i in reversed(range(self.proxy_pages.count())):
            if i == 0:
                return
            widget = self.proxy_pages.widget(i)
            self.proxy_pages.removeWidget(self.proxy_pages.widget(i))
            widget.setParent(None)
