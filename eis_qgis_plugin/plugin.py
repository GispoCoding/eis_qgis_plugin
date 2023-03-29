from typing import Callable, List, Optional

import os

from qgis.PyQt.QtCore import QCoreApplication, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QWidget, QInputDialog, QLineEdit
from qgis.utils import iface
from qgis.core import QgsApplication, QgsProject
from eis_qgis_plugin.settings import get_python_venv_path, save_python_venv_path

from eis_qgis_plugin.qgis_plugin_tools.tools.custom_logging import (
    setup_logger,
    teardown_logger,
)
from eis_qgis_plugin.qgis_plugin_tools.tools.i18n import setup_translation
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import plugin_name

from eis_qgis_plugin.wizard.wizard_main import EISWizardMain
from eis_qgis_plugin.wizard.wizard_preprocess import EISWizardPreprocess
from eis_qgis_plugin.wizard.wizard_explore import EISWizardExplore, EISWizardExploreBig
from eis_qgis_plugin.processing.eis_provider import EISProvider

pluginPath = os.path.dirname(__file__)


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
        self.iface = iface

        # locale = QgsApplication.locale()
        # qmPath = '{}/i18n/wbt_for_qgis_{}.qm'.format(pluginPath, locale)

        # if os.path.exists(qmPath):
        #     self.translator = QTranslator()
        #     self.translator.load(qmPath)
        #     QCoreApplication.installTranslator(self.translator)
        self.provider = EISProvider()

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
            iface.addToolBarIcon(action)

        if add_to_menu:
            iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self) -> None:  # noqa N802
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.add_action(
            "",
            text=Plugin.name,
            callback=self.run,
            parent=iface.mainWindow(),
            add_to_toolbar=True,
        )

        self.add_action(
            os.path.join(pluginPath, 'resources/icons/plugin_icon.png'),  # Some placeholder icon
            text='Set Python Virtual Environment Path',
            parent=iface.mainWindow(),
            add_to_toolbar=True,
            callback=self.set_python_venv_path
        )

        # Add links to Wizard steps as separate buttons, at least for now
        self.add_action(
            "",
            text='EIS Preprocess',
            parent=iface.mainWindow(),
            add_to_toolbar=True,
            callback=self.open_preprocess
        )

        self.add_action(
            "",
            text='EIS Explore',
            parent=iface.mainWindow(),
            add_to_toolbar=True,
            callback=self.open_explore
        )

        self.add_action(
            "",
            text='Add group',
            parent=iface.mainWindow(),
            add_to_toolbar=True,
            callback=self.add_layer_group
        )

        self.initProcessing()

    def initProcessing(self):
        QgsApplication.processingRegistry().addProvider(self.provider)

    def onClosePlugin(self) -> None:  # noqa N802
        """Cleanup necessary items here when plugin dockwidget is closed"""
        pass

    def unload(self) -> None:
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            iface.removePluginMenu(Plugin.name, action)
            iface.removeToolBarIcon(action)
        teardown_logger(Plugin.name)

        QgsApplication.processingRegistry().removeProvider(self.provider)

    def set_python_venv_path(self):
        python_path, ok = QInputDialog.getText(
            self.iface.mainWindow(),
            'Python Virtual Environment Path',
            'Enter the path to your Python virtual environment:',
            QLineEdit.Normal,
            get_python_venv_path()
        )

        if ok and python_path:
            save_python_venv_path(python_path)

    def open_preprocess(self):
        self.preprocess_window = EISWizardPreprocess(iface)
        self.preprocess_window.show()

    def open_explore(self):
        self.explore_window_big = EISWizardExploreBig(iface)
        self.explore_window = EISWizardExplore(iface)
        self.explore_window_big.show()
        self.explore_window.show()

    def log(self, message: str) -> None:
        """Pushes a message to QGIS log."""
        self.iface.messageBar().pushMessage(message)

    # EXPERIMENTS
    def add_layer_group(self):
        root = QgsProject.instance().layerTreeRoot()
        eis_group = root.addGroup("EIS")
        raw_group = eis_group.addGroup("Raw data")
        processed_group = eis_group.addGroup("Processed data")
        granite_group = processed_group.addGroup("Granite data")
        fault_group = processed_group.addGroup("Fault lines data")


    def run(self):
        """Run method that performs all the real work"""
        self.first_start = True
        if self.first_start:
            self.first_start = False
            self.wizard_window = EISWizardMain(iface)

        self.wizard_window.show() # Show the dialog
        # result = self.test_dlg.exec_() # Run the dialog event loop

        # if result:  # See if OK was pressed
        #     self.iface.messageBar().pushMessage('OK pressed. Closing EIS Wizard')
