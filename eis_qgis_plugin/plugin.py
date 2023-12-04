import os
from typing import Callable, List, Optional

from qgis.core import QgsApplication, QgsProject
from qgis.gui import QgisInterface
from qgis.PyQt.QtCore import QCoreApplication, Qt, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QAction,
    QInputDialog,
    QLineEdit,
    QMenu,
    QToolButton,
    QWidget,
)
from qgis.utils import iface

from eis_qgis_plugin.utils import PLUGIN_PATH

from .processing.eis_provider import EISProvider
from .qgis_plugin_tools.tools.custom_logging import setup_logger, teardown_logger
from .qgis_plugin_tools.tools.i18n import setup_translation
from .qgis_plugin_tools.tools.resources import plugin_name
from .settings import get_python_venv_path, save_python_venv_path
from .wizard.explore.wizard_explore import EISWizardExplore
from .wizard.preprocess.wizard_proxy_dock import EISWizardProxyDock
from .wizard.preprocess.wizard_proxy_settings import EISWizardProxySettings
from .wizard.search_test import SearchDialog
from .wizard.wizard_main import EISWizardDialog, EISWizardDocked
from .wizard.wizard_model import EISWizardModeling


class Plugin:
    """QGIS Plugin Implementation."""

    name = plugin_name()

    def __init__(self) -> None:
        setup_logger(Plugin.name)

        # initialize locale
        locale, file_path = setup_translation()
        if file_path:
            self.translator = QTranslator()
            self.translator.load(file_path)
            # noinspection PyCallByClass
            QCoreApplication.installTranslator(self.translator)
        else:
            pass

        self.actions: List[QAction] = []
        self.menu = Plugin.name
        self.iface: QgisInterface = iface

        # locale = QgsApplication.locale()
        # qmPath = '{}/i18n/wbt_for_qgis_{}.qm'.format(pluginPath, locale)

        # if os.path.exists(qmPath):
        #     self.translator = QTranslator()
        #     self.translator.load(qmPath)
        #     QCoreApplication.installTranslator(self.translator)

    def add_action(
        self,
        icon_path: str,
        text: str,
        callback: Callable,
        enabled_flag: bool = True,
        add_to_menu: bool = True,
        add_to_toolbar: bool = True,
        status_tip: Optional[str] = None,
        whats_this: Optional[str] = None,
        parent: Optional[QWidget] = None,
    ) -> QAction:
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.

        :param text: Text that should be shown in menu items for this action.

        :param callback: Function to be called when the action is triggered.

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.

        :param parent: Parent widget for the new action. Defaults None.

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        # noinspection PyUnresolvedReferences
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self) -> None:  # noqa N802
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        # icon_path = os.path.join(pluginPath, "resources/icons/plugin_icon.png")  # A placeholder icon
        icon_path = os.path.join(
            PLUGIN_PATH, "resources/icons/icon4.png"
        )  # A placeholder icon

        # main_action = self.add_action(
        #     icon_path,
        #     text="EIS Wizard Main",
        #     callback=self.run,
        #     parent=self.iface.mainWindow(),
        #     add_to_toolbar=False,
        #     add_to_menu=False
        # )

        self.add_action(
            "",
            text="Settings",
            callback=self.set_python_venv_path,
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
            add_to_menu=True,
        )

        # Add links to Wizard steps as separate buttons, at least for now
        wizard_action = self.add_action(
            icon_path,
            text="EIS Wizard",
            parent=self.iface.mainWindow(),
            callback=self.open_wizard_dialog,
            add_to_toolbar=False,
            add_to_menu=False,
        )

        self.add_action(
            "",
            text="Mineral system proxies",
            parent=self.iface.mainWindow(),
            callback=self.open_proxy_settings,
            add_to_toolbar=False,
            add_to_menu=True,
        )

        self.add_action(
            "",
            text="Explore",
            parent=self.iface.mainWindow(),
            callback=self.open_explore,
            add_to_toolbar=False,
            add_to_menu=True,
        )

        self.add_action(
            "",
            text="Modeling",
            parent=self.iface.mainWindow(),
            callback=self.open_modeling,
            add_to_toolbar=False,
            add_to_menu=True,
        )

        self.add_action(
            "",
            text="Mineral system proxies DOCK version",
            parent=self.iface.mainWindow(),
            callback=self.open_proxy_dock_widget,
            add_to_toolbar=False,
            add_to_menu=True,
        )

        self.add_action(
            "",
            text="Docked full wizard",
            parent=self.iface.mainWindow(),
            callback=self.open_wizard_dock,
            add_to_toolbar=False,
            add_to_menu=True,
        )

        self.add_action(
            "",
            text="Testing: Add group",
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
            add_to_menu=True,
            callback=self.add_layer_group,
        )

        self.add_action(
            "",
            text="Testing: Open search",
            parent=self.iface.mainWindow(),
            callback=self.open_search,
            add_to_toolbar=False,
            add_to_menu=True,
        )

        self.popupMenu = QMenu(self.iface.mainWindow())
        self.popupMenu.addAction(wizard_action)
        # self.popupMenu.addAction(preprocess_action)
        # self.popupMenu.addAction(explore_action)
        # self.popupMenu.addAction(model_action)
        # self.popupMenu.addAction(venv_action)
        # self.popupMenu.addAction(open_dock_action)
        # self.popupMenu.addAction(search_action)
        # self.popupMenu.addAction(group_action)

        self.toolButton = QToolButton()
        self.toolButton.setMenu(self.popupMenu)
        self.toolButton.setDefaultAction(wizard_action)
        self.toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.actions.append(self.iface.addToolBarWidget(self.toolButton))

        self.initProcessing()

    def initProcessing(self):
        self.provider = EISProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def onClosePlugin(self) -> None:  # noqa N802
        """Cleanup necessary items here when plugin dockwidget is closed"""
        pass

    def unload(self) -> None:
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(Plugin.name, action)
            self.iface.removeToolBarIcon(action)
        teardown_logger(Plugin.name)

        QgsApplication.processingRegistry().removeProvider(self.provider)

    def set_python_venv_path(self):
        python_path, ok = QInputDialog.getText(
            self.iface.mainWindow(),
            "Python Virtual Environment Path",
            "Enter the path to your Python virtual environment:",
            QLineEdit.Normal,
            get_python_venv_path(),
        )

        if ok and python_path:
            save_python_venv_path(python_path)

    def open_wizard_dialog(self):
        self.wizard = EISWizardDialog()
        self.wizard.show()

    def open_wizard_dock(self):
        self.wizard = EISWizardDocked()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.wizard)

    def open_proxy_settings(self):
        self.proxy_settings_window = EISWizardProxySettings()
        self.proxy_settings_window.show()

    def open_explore(self):
        self.explore_window = EISWizardExplore()
        self.explore_window.show()

    def open_modeling(self):
        self.model_window = EISWizardModeling()
        self.model_window.show()

    def open_proxy_dock_widget(self):
        self.dock_widget = EISWizardProxyDock()
        # connect to provide cleanup on closing of dockwidget

        # show the dockwidget
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        # self.dock_widget.show()
        # self.dock_widget. # TODO

    def open_search(self):
        self.search_dialog = SearchDialog()
        self.search_dialog.show()

    def log(self, message: str) -> None:
        """Pushes a message to QGIS log."""
        self.iface.messageBar().pushMessage(message)

    # EXPERIMENTS
    def add_layer_group(self):
        root = QgsProject.instance().layerTreeRoot()
        eis_group = root.addGroup("EIS")
        _ = eis_group.addGroup("Raw data")
        processed_group = eis_group.addGroup("Processed data")
        _ = processed_group.addGroup("Granite data")
        _ = processed_group.addGroup("Fault lines data")

    def run(self):
        """Run method that performs all the real work"""
        self.first_start = True
        if self.first_start:
            self.first_start = False
            pass

        # result = self.test_dlg.exec_() # Run the dialog event loop

        # if result:  # See if OK was pressed
        #     self.iface.messageBar().pushMessage('OK pressed. Closing EIS Wizard')
