import os

from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtWidgets import QDialog, QLabel, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils import PLUGIN_PATH

FORM_CLASS: QDialog = load_ui("wizard_about.ui")


class EISWizardAbout(QWidget, FORM_CLASS):

    gnu_logo_label: QLabel

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        gnu_pixmap = QPixmap(os.path.join(PLUGIN_PATH, "resources/icons/gnu_logo.png"))
        self.gnu_logo_label.setPixmap(gnu_pixmap)
