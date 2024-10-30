import os
from typing import Callable, List, Optional

from qgis.core import QgsApplication
from qgis.gui import QgisInterface
from qgis.PyQt.QtCore import QCoreApplication, Qt, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu, QToolButton, QWidget
from qgis.utils import iface

from eis_qgis_plugin.eis_processing.eis_provider import EISProvider
from eis_qgis_plugin.qgis_plugin_tools.tools.custom_logging import setup_logger, teardown_logger
from eis_qgis_plugin.utils.misc_utils import PLUGIN_PATH
from eis_qgis_plugin.utils.settings_manager import EISSettingsManager

from .eis_wizard.wizard_main import EISWizardDialog, EISWizardDocked
from .qgis_plugin_tools.tools.i18n import setup_translation


class Plugin:
    """QGIS Plugin Implementation."""

    name = "EIS QGIS Plugin"

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
        icon_path = os.path.join(PLUGIN_PATH, "resources/icons/icon4.png")  # A placeholder icon

        wizard_action = self.add_action(
            icon_path,
            text="EIS Wizard",
            parent=self.iface.mainWindow(),
            callback=lambda: self.open_wizard(0),
            add_to_toolbar=False,
            add_to_menu=True,
        )

        env_action = self.add_action(
            "",
            text="Set EIS Toolkit env",
            parent=self.iface.mainWindow(),
            callback=lambda: self.open_wizard(4),
            add_to_toolbar=False,
            add_to_menu=True,
        )

        self.initProcessing()

        self.popupMenu = QMenu(self.iface.mainWindow())
        self.popupMenu.addAction(wizard_action)
        self.popupMenu.addAction(env_action)

        self.toolButton = QToolButton()
        self.toolButton.setMenu(self.popupMenu)
        self.toolButton.setDefaultAction(wizard_action)
        self.toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.actions.append(self.iface.addToolBarWidget(self.toolButton))


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

    def open_wizard(self, page):
        if EISSettingsManager.get_dock_wizard_selection():
            self.open_wizard_dock(page)
        else:
            self.open_wizard_dialog(page)

    def open_wizard_dialog(self, page):
        self.wizard = EISWizardDialog()
        self.wizard.show()
        self.wizard.content.menu_widget.setCurrentRow(page)

    def open_wizard_dock(self, page):
        self.wizard = EISWizardDocked()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.wizard)
        self.wizard.content.menu_widget.setCurrentRow(page)
