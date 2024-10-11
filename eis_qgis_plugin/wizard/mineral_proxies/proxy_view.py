import os
from typing import List, Optional

from qgis.core import QgsApplication
from qgis.gui import QgsFilterLineEdit
from qgis.PyQt.QtGui import QFont, QIcon
from qgis.PyQt.QtWidgets import QComboBox, QGridLayout, QLabel, QMenu, QPushButton, QSizePolicy, QWidget
from qgis.utils import iface

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.misc_utils import PLUGIN_PATH
from eis_qgis_plugin.wizard.mineral_proxies.configuration_dialogs.define_proxy import EISWizardDefineProxy
from eis_qgis_plugin.wizard.mineral_proxies.mineral_system import MineralProxy, MineralSystem, ProxyImportance

FORM_CLASS = load_ui("mineral_proxies/proxy_view3.ui")

# SETTINGS
COLOR_CODE_CATEGORIES = True
CATEGORY_COLORS = {
    "geology": "sandybrown",
    "geophysics": "blue",
    "geochemistry": "green",
}


class EISWizardProxyView(QWidget, FORM_CLASS):

    def __init__(
        self,
        proxy_manager: QWidget,
        mineral_systems: List[MineralSystem],
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # DELCARE TYPES
        self.scale_selection: QComboBox
        self.mineral_system_selection: QComboBox
        self.configure_mineral_systems_btn: QPushButton

        self.configure_proxies_btn: QPushButton
        self.search_bar: QgsFilterLineEdit

        self.source_grid_layout: QGridLayout
        self.pathway_grid_layout: QGridLayout
        self.depositional_grid_layout: QGridLayout
        self.mineralisation_grid_layout: QGridLayout
        self.grid_layouts = {
            "source": self.source_grid_layout,
            "pathway": self.pathway_grid_layout,
            "depositional": self.depositional_grid_layout,
            "mineralisation": self.mineralisation_grid_layout
        }

        # Initialize attributes and widgets
        self.proxy_manager = proxy_manager

        self.mineral_systems = mineral_systems
        for mineral_system in self.mineral_systems:
            self.mineral_system_selection.addItem(mineral_system.name)
        self.mineral_system_selection.setCurrentIndex(0)
        self.selected_mineral_system = self.mineral_systems[0]

        self.selected_scale = self.scale_selection.currentText().lower()

        self.widgets_per_proxy = {}

        # Initialize UI
        # Bold font
        self.bold_font = QFont()
        self.bold_font.setBold(True)

        self.conf_icon = QIcon(os.path.join(PLUGIN_PATH, "resources/icons/settings.svg"))

        # Mineral system configuration menu
        conf_mineral_systems_menu = QMenu()
        self.new_action = conf_mineral_systems_menu.addAction(
            QgsApplication.getThemeIcon('symbologyAdd.svg'), "New"
        )
        self.delete_action = conf_mineral_systems_menu.addAction(
            QgsApplication.getThemeIcon('mActionDeleteSelected.svg'), "Delete"
        )
        self.import_action = conf_mineral_systems_menu.addAction(
            QgsApplication.getThemeIcon('mActionFileOpen.svg'), "Import"
        )
        self.export_action = conf_mineral_systems_menu.addAction(
            QgsApplication.getThemeIcon('mActionFileSaveAs.svg'), "Export"
        )
        self.configure_mineral_systems_btn.setMenu(conf_mineral_systems_menu)
        self.configure_mineral_systems_btn.setIcon(self.conf_icon)

        # Proxies menu
        configure_proxy_menu = QMenu()
        self.define_proxy_action = configure_proxy_menu.addAction(
            QgsApplication.getThemeIcon('symbologyAdd.svg'), "Define new proxy"
        )
        self.import_proxy_action = configure_proxy_menu.addAction(
            QgsApplication.getThemeIcon('mActionFileOpen.svg'), "Add proxy from another mineral system"
        )
        self.edit_proxy_action = configure_proxy_menu.addAction(
            QgsApplication.getThemeIcon("mActionToggleEditing.svg"), "Edit custom proxies"
        )
        self.delete_proxy_action = configure_proxy_menu.addAction(
            QgsApplication.getThemeIcon("mActionDeleteSelected.svg"), "Delete custom proxies"
        )
        self.configure_proxies_btn.setMenu(configure_proxy_menu)
        self.configure_proxies_btn.setIcon(self.conf_icon)

        # Proxy view itself
        self.create_view()

        # Connect signals
        self.search_bar.textChanged.connect(self.filter_proxies)
        self.scale_selection.currentTextChanged.connect(self._on_settings_changed)
        self.mineral_system_selection.currentTextChanged.connect(self._on_settings_changed)

        self.new_action.triggered.connect(self._on_new_mineral_system_clicked)
        self.delete_action.triggered.connect(self._on_delete_mineral_system_clicked)
        self.import_action.triggered.connect(self._on_import_mineral_system_clicked)
        self.export_action.triggered.connect(self._on_export_mineral_system_clicked)

        self.define_proxy_action.triggered.connect(self._on_define_proxy_clicked)
        self.import_proxy_action.triggered.connect(self._on_import_proxy_clicked)
        self.edit_proxy_action.triggered.connect(self._on_edit_proxy_clicked)
        self.delete_proxy_action.triggered.connect(self._on_delete_proxy_clicked)


    def _on_new_mineral_system_clicked(self):
        print("NEW TEST")

    def _on_delete_mineral_system_clicked(self):
        print("DEL TEST")

    def _on_import_mineral_system_clicked(self):
        print("IMPORT TEST")

    def _on_export_mineral_system_clicked(self):
        print("EXPORT TEST")

    def _on_define_proxy_clicked(self):
        dlg = EISWizardDefineProxy(self)
        dlg.show()

    def _on_import_proxy_clicked(self):
        print("IMPORT PROXY TEST")

    def _on_edit_proxy_clicked(self):
        print("EDIT TEST")

    def _on_delete_proxy_clicked(self):
        print("DEL PROXY TEST")


    def _on_settings_changed(self):
        self.selected_mineral_system = self.mineral_systems[self.mineral_system_selection.currentIndex()]
        self.selected_scale = self.scale_selection.currentText().lower()

        self.clear_view()
        self.create_view()


    def sort_proxies(self, proxies: List[MineralProxy]) -> List[MineralProxy]:
        """Sort proxies by importance primarily and by name secondarily."""
        if self.selected_scale == "regional":
            return sorted(proxies, key=lambda proxy: (proxy.regional_scale_importance.value, proxy.name))
        elif self.selected_scale == "camp":
            return sorted(proxies, key=lambda proxy: (proxy.camp_scale_importance.value, proxy.name))
        elif self.selected_scale == "deposit":
            return sorted(proxies, key=lambda proxy: (proxy.deposit_scale_importance.value, proxy.name))
        else:
            raise Exception(f"Sorting proxies but unrecognized scale: {self.selected_scale}.")


    def create_view(self):
        """Create new tables for each tab with selected mineral system and scale."""    
        # 2 mineral systems not implemented yet, display messages
        if self.selected_mineral_system.name == "Li-Pegmatites":
            iface.messageBar().pushWarning(
                "Error: ", "Li-Pegmatites proxies are not implemented in EIS QGIS plugin yet."
            )
            return
        elif self.mineral_system_selection.currentText() == "Co-VMS":
            iface.messageBar().pushWarning("Error: ", "Co-VMS proxies are not implemented in EIS QGIS plugin yet.")
            return

        # Create header rows
        for _, layout in self.grid_layouts.items():
            name_label = QLabel("Proxy")
            name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
            name_label.setWordWrap(True)
            name_label.setFont(self.bold_font)
            layout.addWidget(name_label, 0, 1)

            category_label = QLabel("Category")
            category_label.setFont(self.bold_font)
            layout.addWidget(category_label, 0, 2)

        # Create proxy entries
        proxies = self.sort_proxies(self.selected_mineral_system.proxies)
        for i, proxy in enumerate(proxies):
            proxy.mineral_system_component
            self.create_proxy_row(proxy=proxy, row=i)


    def create_proxy_row(self, proxy: MineralProxy, row: int):
        """Create a new row in the proxy table."""
        row = row + 1  # Account for header row
        component = proxy.mineral_system_component
        layout = self.grid_layouts[component]

        widgets = []
        # 0. Importance
        importance = proxy.importance_from_scale(self.selected_scale)
        if importance.value != 4:
            importance_label = self.create_importance_widget(importance)
            layout.addWidget(importance_label, row, 0)
            widgets.append(importance_label)

        # 1. Name label
        name_label = QLabel(proxy.name)
        name_label.setWordWrap(True)
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(name_label, row, 1)

        # 2. Category label
        category = proxy.category
        if COLOR_CODE_CATEGORIES:
            category_label = QLabel()
            category_text = ""
            if proxy.category in CATEGORY_COLORS.keys():
                category_text += (
                    f"<span style='color: {CATEGORY_COLORS[category]};'>{category}</span>, "
                )
            else:
                category_text += f"{category}, "
            category_text = category_text[:-2]
            category_label.setText("<html><body>" + category_text + "</body></html>")
        else:
            category_label = QLabel(category)
        category_label.setWordWrap(True)
        layout.addWidget(category_label, row, 2)

        # 3. Process button
        process_button = QPushButton("Process")
        process_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        process_button.clicked.connect(
            lambda: self.proxy_manager.enter_proxy_processing(self.selected_mineral_system.name, proxy)
        )
        layout.addWidget(process_button, row, 3)

        self.widgets_per_proxy[proxy.name] = (proxy, widgets + [name_label, category_label, process_button])


    def create_importance_widget(self, importance: ProxyImportance) -> QLabel:
        importance_label = QLabel("*")
        importance_label.setStyleSheet(f"color: {importance.color_coding};")
        importance_label.setToolTip(importance.tooltip_text)
        return importance_label


    def filter_proxies(self, search_text: str):
        """Updates proxy table based on search."""
        for proxy_name, (proxy, widgets) in self.widgets_per_proxy.items():
            if (
                search_text.lower() in proxy_name.lower()
                or any(search_text.lower() in word.lower() for word in proxy.category.lower())
            ):
                [widget.show() for widget in widgets]
            else:
                [widget.hide() for widget in widgets]


    def clear_view(self):
        """Clears proxy table row widgets."""
        self.search_bar.clear()
        for layout in self.grid_layouts.values():
            for i in reversed(range(layout.count())):
                widget = layout.takeAt(i).widget()
                if widget is not None:
                    layout.removeWidget(widget)
                    widget.setParent(None)

        # Clear the widget dictionary
        self.widgets_per_proxy.clear()
