
from qgis.PyQt.QtWidgets import QDialog, QLabel, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QDialog = load_ui("wizard_about.ui")


class EISWizardAbout(QWidget, FORM_CLASS):

    eupl_logo_label: QLabel

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # eupl_pixmap = QPixmap(os.path.join(PLUGIN_PATH, "resources/icons/logo_EUPL_small.png"))
        # self.eupl_logo_label.setPixmap(eupl_pixmap)
