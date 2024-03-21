import json
import os
from typing import Dict, List, Optional, Tuple

from qgis.PyQt import QtGui
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from qgis.utils import iface

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils import PLUGIN_PATH

FORM_CLASS = load_ui("mineral_proxies/proxy_view.ui")


class EISWizardProxyView(QWidget, FORM_CLASS):

    PROXY_DATA_PATH = os.path.join(PLUGIN_PATH, "resources/proxies.json")
    PROXY_CATEGORIES = ["source", "pathway", "depositional", "mineralisation"]
    CATEGORY_COLORS = {
        "geology": "sandybrown",
        "geophysics": "blue",
        "geochemistry": "green",
    }
    IMPORTANCES = {
        "High": {"value": 1, "style_sheet": "color: red;", "tooltip": "Importance: High"},
        "Moderate": {"value": 2, "style_sheet": "color: orange;", "tooltip": "Importance: Moderate"},
        "Low": {"value": 3, "style_sheet": "color: green;", "tooltip": "Importance: Low"},
        "-": {"value": 4, "style_sheet": "color: black;", "tooltip": "Importance: Not defined"}
    }


    def __init__(
        self,
        proxy_manager: QWidget,
        parent: Optional[QWidget] = None,
        color_importance = True,
        color_category = True
    ) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.proxy_manager = proxy_manager
        self.color_importance = color_importance
        self.color_category = color_category

        # DELCARE TYPES
        self.scale_selection: QComboBox
        self.mineral_system_selection: QComboBox

        self.tabs: QTabWidget
        self.source_tab: QWidget
        self.pathway_tab: QWidget
        self.depositional_tab: QWidget
        self.mineralisation_tab: QWidget

        # Initialize
        self.connect_signals()
        self.initialize_data()
        self.initialize_ui()
        self.create_tables()


    def connect_signals(self):
        self.scale_selection.currentTextChanged.connect(self._on_settings_changed)
        self.mineral_system_selection.currentTextChanged.connect(self._on_settings_changed)


    def initialize_data(self):
        self.proxy_info: Dict[str, Tuple[List[str], List[QWidget]]] = {}
        self.tabs = [
            self.source_tab,
            self.pathway_tab,
            self.depositional_tab,
            self.mineralisation_tab
        ]
        with open(self.PROXY_DATA_PATH, "r") as file:
            self.proxy_data = json.loads(file.read())


    def initialize_ui(self):
        """Initialize the UI."""
        # Create bold font
        self.bold_font = QtGui.QFont()
        self.bold_font.setBold(True)

        self.grid_layouts = {}
        for tab, category in zip(self.tabs, self.PROXY_CATEGORIES):
            tab_layout = QVBoxLayout()

            # Create and add search layout and widget
            search_layout = QHBoxLayout()
            search_label = QLabel("Search")
            search_bar = QLineEdit()
            search_bar.textChanged.connect(self.filter_proxies)
            search_layout.addWidget(search_label)
            search_layout.addWidget(search_bar)
            tab_layout.addLayout(search_layout)

            # Create and add proxy table layout and widget
            grid_layout = QGridLayout()
            self.grid_layouts[category] = (grid_layout, search_bar)

            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout()
            scroll_layout.addLayout(grid_layout)
            scroll_layout.addStretch()
            scroll_widget.setLayout(scroll_layout)
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(scroll_widget)
            tab_layout.addWidget(scroll_area)

            tab.setLayout(tab_layout)


    def _on_settings_changed(self):
        self.clear_tables()
        self.create_tables()


    def get_proxies_custom(self, category: str) -> dict:
        """
        Custom mineral system uses all proxies from all mineral systems.
        
        Duplicates are ignored. Proxies are sorted alphabetically.
        """
        proxies = {
            **self.proxy_data["iocg"][category],
            **self.proxy_data["li-pegmatites"][category],
            **self.proxy_data["co-vms"][category]
        }
        return self.sort_proxies_alphabetically(proxies)
       
    
    def sort_proxies_alphabetically(self, proxies: dict) -> dict:
        return dict(
            sorted(
                proxies.items()
            )
        )


    def get_proxies(self, mineral_system: str, category: str, scale: str) -> dict:
        return self.sort_proxies_by_importance(mineral_system, category, scale)


    def sort_proxies_by_importance(self, mineral_system: str, category: str, scale: str) -> dict:
        return dict(
            sorted(
                self.proxy_data[mineral_system][category].items(),
                key=lambda proxy: self.IMPORTANCES[proxy[1]["importance"][scale]]["value"]
            )
        )


    def get_proxy_view_settings(self) -> Tuple[str, str]:
        return self.mineral_system_selection.currentText().lower(), self.scale_selection.currentText().lower()
    

    def get_proxies_for_category(self, category, mineral_system, scale):
        if mineral_system == "custom":
            sorted_proxies = self.get_proxies_custom(category)
        else:
            sorted_proxies = self.get_proxies(mineral_system, category, scale)

        return sorted_proxies


    def create_table_for_category(self, proxies, mineral_system, scale, grid_layout):
        # Create label row
        self.create_table_row(grid_layout, 0, "Proxy", "Importance", "Category", "Workflow", label=True)

        # Create proxy rows
        for i, (proxy_name, proxy_details) in enumerate(proxies.items()):
            self.create_table_row(
                grid_layout=grid_layout,
                row=i+1,  # +1 because of label row
                name=proxy_name,
                importance=proxy_details["importance"][scale] if mineral_system != "custom" else "",
                category=proxy_details["category"],
                workflow=proxy_details["workflow"]
            )


    def create_tables(self):
        """Create new tables for each tab with selected mineral system and scale."""
        mineral_system, scale = self.get_proxy_view_settings()
        # 2 mineral systems not implemented yet, display messages
        if mineral_system == "li-pegmatites (not implemented)":
            iface.messageBar().pushWarning("Error: ", "Li-Pegmatites proxies are not included in EIS QGIS plugin yet.")
            return
        elif mineral_system == "co-vms (not implemented)":
            iface.messageBar().pushWarning("Error: ", "Co-VMS proxies are not included in EIS QGIS plugin yet.")
            return

        # Populate tab at a time
        for category in self.PROXY_CATEGORIES:
            grid_layout, _ = self.grid_layouts[category]

            proxies = self.get_proxies_for_category(category, mineral_system, scale)

            self.create_table_for_category(proxies, mineral_system, scale, grid_layout)


    def create_table_row(
        self,
        grid_layout: QGridLayout,
        row: int,
        name: str,
        importance: str,
        category: str,
        workflow: str,
        label=False,
    ):
        """Create a new row in the proxy table."""
        # 0. Importance
        importance_label = QLabel("*")
        if importance != "Importance" and importance != "":
            style_sheet = self.IMPORTANCES[importance].get("style_sheet", None)
            if style_sheet:
                importance_label.setStyleSheet(style_sheet)

            tooltip = self.IMPORTANCES[importance].get("tooltip", None)
            if tooltip:
                importance_label.setToolTip(tooltip)

            grid_layout.addWidget(importance_label, row, 0)

        # 1. Name label
        name_label = QLabel(name)
        name_label.setWordWrap(True)
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        grid_layout.addWidget(name_label, row, 1)

        # 2. Category label
        if self.color_category:
            category_label = QLabel()
            category_text = ""
            if category in self.CATEGORY_COLORS.keys():
                category_text += (
                    f"<span style='color: {self.CATEGORY_COLORS[category]};'>{category}</span>, "
                )
            else:
                category_text += f"{category}, "
            category_text = category_text[:-2]
            category_label.setText("<html><body>" + category_text + "</body></html>")
        else:
            category_label = QLabel(category)
        category_label.setWordWrap(True)
        grid_layout.addWidget(category_label, row, 2)

        if label:
            name_label.setFont(self.bold_font)
            category_label.setFont(self.bold_font)
        else:
            # 3. Process button
            process_button = QPushButton("Process")
            process_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            process_button.clicked.connect(lambda: self.proxy_manager.enter_proxy_processing(int(workflow)))
            grid_layout.addWidget(process_button, row, 3)

            self.proxy_info[name] = (category, [name_label, importance_label, category_label, process_button])


    def filter_proxies(self, search_text: str):
        """Updates proxy table based on search."""
        for proxy_name, (category, widgets) in self.proxy_info.items():
            if (
                search_text.lower() in proxy_name.lower()
                or any(search_text.lower() in word.lower() for word in category)
            ):
                [widget.show() for widget in widgets]
            else:
                [widget.hide() for widget in widgets]


    def clear_tables(self):
        """Clears proxy table row widgets."""
        for layout, search_bar in self.grid_layouts.values():
            search_bar.clear()
            for i in reversed(range(layout.count())):
                widget = layout.takeAt(i).widget()
                if widget is not None:
                    layout.removeWidget(widget)
                    widget.setParent(None)

        # Clear the dictionary
        self.proxy_info.clear()
