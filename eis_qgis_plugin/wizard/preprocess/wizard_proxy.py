from qgis.PyQt.QtWidgets import QWizard

from .wizard_proxy_selection_page import EISWizardProxySelection
from .wizard_proxy_creation_page import EISWizardProxyCreation


class EISWizardProxy(QWizard):
    def __init__(self, study_scale, mineral_system, parent=None):
        super().__init__(parent)

        self.setWindowTitle(
            f"EIS Mineral system proxies --- Mineral system: {mineral_system}, Study scale: {study_scale}"
        )

        self.resize(830, 520)

        self.page1 = EISWizardProxySelection(study_scale, mineral_system)
        self.page2 = EISWizardProxyCreation()

        self.addPage(self.page1)
        self.addPage(self.page2)

        self.setOption(QWizard.NoDefaultButton, on=True)

        self.setButtonText(QWizard.BackButton, "Back to proxy list")
        self.setButtonText(QWizard.CancelButton, "Close")

        layout = [QWizard.Stretch, QWizard.BackButton, QWizard.CancelButton]
        self.setButtonLayout(layout)

        # self.currentIdChanged.connect(self.handle_current_id_changed)

    # def handle_current_id_changed(self):
    #     if id == 0:  # Page 0
    #         self.my_custom_button_1.hide()
    #         self.my_custom_button_2.show()
    #     elif id == 1:  # Page 1
    #         self.my_custom_button_1.show()
    #         self.my_custom_button_2.hide()
