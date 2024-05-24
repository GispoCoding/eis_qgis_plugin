from qgis.PyQt.QtWidgets import (
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from eis_qgis_plugin.wizard.mineral_proxies.proxy_processing import (
    # EISWizardProxyDefineAnomaly,
    EISWizardProxyDistanceToFeatures,
    EISWizardProxyInterpolateAndDefineAnomaly,
)

# EISWizardProxyInterpolation,
from eis_qgis_plugin.wizard.mineral_proxies.proxy_view import EISWizardProxyView


class EISWizardProxies(QWidget):

    # CATEGORY_PROCESS_MAP = {
    #     "geochemistry": EISWizardProxyInterpolation,
    #     "geology": EISWizardProxyDistanceToFeatures,
    #     "geophysics": EISWizardProxyDefineAnomaly,
    #     "test": EISWizardProxyInterpolateAndDefineAnomaly
    # }
    WORKFLOW_MAP = {
        1: EISWizardProxyDistanceToFeatures,
        # 2: EISWizardProxyInterpolation,
        # 3: EISWizardProxyDefineAnomaly,
        4: EISWizardProxyInterpolateAndDefineAnomaly
    }

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.proxy_view = EISWizardProxyView(proxy_manager=self)
        self.proxy_pages = QStackedWidget(self)
        self.proxy_pages.addWidget(self.proxy_view)

        layout = QVBoxLayout()
        layout.addWidget(self.proxy_pages)
        self.setLayout(layout)


    def enter_proxy_processing(self, mineral_system: str, category: str, proxy_name: str, workflow: int):
        processing_page = self.WORKFLOW_MAP[workflow](self, mineral_system, category, proxy_name)
        self.proxy_pages.addWidget(processing_page)
        self.proxy_pages.setCurrentIndex(1)


    def return_from_proxy_processing(self):
        self.proxy_pages.setCurrentIndex(0)
        self.delete_proxy_processing_page()


    def delete_proxy_processing_page(self):
        for i in reversed(range(self.proxy_pages.count())):
            if i == 0:
                return
            widget = self.proxy_pages.widget(i)
            self.proxy_pages.removeWidget(self.proxy_pages.widget(i))
            widget.setParent(None)
