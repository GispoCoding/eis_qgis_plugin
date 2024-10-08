import os

from qgis.gui import QgsDockWidget
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QDialog, QListWidget, QListWidgetItem, QStackedWidget, QVBoxLayout, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.misc_utils import PLUGIN_PATH
from eis_qgis_plugin.utils.settings_manager import EISSettingsManager
from eis_qgis_plugin.wizard.modeling.model_manager import ModelManager
from eis_qgis_plugin.wizard.wizard_about import EISWizardAbout
from eis_qgis_plugin.wizard.wizard_eda import EISWizardEDA
from eis_qgis_plugin.wizard.wizard_history import EISWizardHistory
from eis_qgis_plugin.wizard.wizard_modeling import EISWizardModeling
from eis_qgis_plugin.wizard.wizard_proxies import EISWizardProxies
from eis_qgis_plugin.wizard.wizard_settings import EISWizardSettings


class EISWizardDialog(QDialog):

    def __init__(self) -> None:
        super().__init__()

        # Default size
        self.resize(1000, 850)

        self.content = EISWizard()

        layout = QVBoxLayout()
        layout.addWidget(self.content)

        self.setLayout(layout)

        self.setWindowTitle("EIS Wizard")


class EISWizardDocked(QgsDockWidget):

    def __init__(self) -> None:
        super().__init__()

        self.content = EISWizard()
        self.setWidget(self.content)

        self.setWindowTitle("EIS Wizard")



FORM_CLASS: QWidget = load_ui("wizard.ui")

class EISWizard(QWidget, FORM_CLASS):

    menu_widget: QListWidget
    pages_widget: QStackedWidget

    menu_items = [
        # Icon: <a href="https://icons8.com/icon/9FSQ5judlnAN/rock">Rock</a>
        # icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        ("Mineral system proxies", QIcon(os.path.join(PLUGIN_PATH, "resources/icons/rock1.png"))),
        
        # Icon: <a href="https://www.flaticon.com/free-icons/data-analysis"
        # title="data analysis icons">Data analysis icons created by HAJICON - Flaticon</a>
        ("EDA", QIcon(os.path.join(PLUGIN_PATH, "resources/icons/eda.png"))),

        # Icon by Icons8
        ("Modeling", QIcon(os.path.join(PLUGIN_PATH, "resources/icons/modeling.png"))),

        # Icon 2: <a href="https://www.flaticon.com/free-icons/history" title="history icons">
        # History icons created by Irfansusanto20 - Flaticon</a>
        ("History", QIcon(os.path.join(PLUGIN_PATH, "resources/icons/history2.png"))),

        # Icon by Icons8
        ("Settings", QIcon(os.path.join(PLUGIN_PATH, "resources/icons/settings.svg"))),

        # Icon by Icons8
        ("About", QIcon(os.path.join(PLUGIN_PATH, "resources/icons/about.svg"))),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.create_menu(EISSettingsManager.get_minimal_menu_selection())

        self.model_manager = ModelManager()

        # Add pages

        # Create Settings page first
        self.settings_page = EISWizardSettings(self)
        self.pages_widget.insertWidget(4, self.settings_page)

        self.proxies_page = EISWizardProxies(self)
        self.pages_widget.insertWidget(0, self.proxies_page)

        self.eda_page = EISWizardEDA(self)
        self.pages_widget.insertWidget(1, self.eda_page)

        self.model_page = EISWizardModeling(self, self.model_manager)
        self.pages_widget.insertWidget(2, self.model_page)
        # self.pages_widget.insertWidget(2, QWidget())

        self.history_page = EISWizardHistory(self, self.model_manager)
        self.pages_widget.insertWidget(3, self.history_page)

        self.about_page = EISWizardAbout(self)
        self.pages_widget.insertWidget(5, self.about_page)

        # Set menu
        # self.menu_widget.setMinimumWidth(
        #     self.menu_widget.sizeHintForColumn(0) + 5)

        self.menu_widget.currentRowChanged['int'].connect(
            self.pages_widget.setCurrentIndex)

        self.menu_widget.setCurrentRow(0)

        # Connect settings signal
        self.settings_page.minimal_menu_setting_changed.connect(self.create_menu)


    def create_menu(self, minimize_text: bool = False):
        for i, (text, icon) in enumerate(self.menu_items):
            item: QListWidgetItem = self.menu_widget.item(i)
            item.setIcon(icon)
            if minimize_text:
                item.setText("")
                self.menu_widget.setMinimumWidth(45)
                self.menu_widget.setMaximumWidth(45)
            else:
                item.setText(text)
                self.menu_widget.setMinimumWidth(210)
                self.menu_widget.setMaximumWidth(210)
