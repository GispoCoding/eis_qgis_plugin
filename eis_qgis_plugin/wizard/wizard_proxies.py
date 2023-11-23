import json
import os

from typing import Dict, List, Tuple

from qgis.PyQt import QtGui
from qgis.PyQt.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QTabWidget
)


from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils import PLUGIN_PATH

FORM_CLASS = load_ui("wizard_proxies.ui")


COLOR_CODE_IMPORTANCE = True
COLOR_CODE_KEYWORDS = True
PROXY_CATEGORIES = ["source", "pathway", "depositional", "mineralisation"]

IMPORTANCE_VALUES = {
    "High": 1,
    "Moderate": 2,
    "Low": 3,
    "-": 4
}


class EISWizardProxies(QWidget, FORM_CLASS):
    scale_selection: QComboBox
    mineral_system_selection: QComboBox

    # Tab widgets
    source_tab_dock: QTabWidget
    pathway_tab_dock: QTabWidget
    depositional_tab_dock: QTabWidget
    mineralisation_tab_dock: QTabWidget

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # Set bold font
        self.bold_font = QtGui.QFont()
        self.bold_font.setBold(True)

        # Connect signals
        self.scale_selection.currentTextChanged.connect(self.update)
        self.mineral_system_selection.currentTextChanged.connect(self.update)

        self.proxy_info: Dict[str, Tuple[List[str], List[QWidget]]] = {}
        self.tab_widgets = [
            self.source_tab_dock,
            self.pathway_tab_dock,
            self.depositional_tab_dock,
            self.mineralisation_tab_dock
        ]

        # Initialize UI
        self.initialize_ui()
        self.update()


    def initialize_ui(self):
        """Initialize the UI."""
        self.grid_layouts = {}
        for tab in self.tab_widgets:
            tab_layout = QVBoxLayout()

            # Create and add search layout and widget
            search_layout = QHBoxLayout()
            search_label = QLabel("Search")
            search_bar = QLineEdit()
            search_bar.textChanged.connect(self.update_table)
            search_layout.addWidget(search_label)
            search_layout.addWidget(search_bar)
            tab_layout.addLayout(search_layout)

            # Create and add proxy table layout and widget
            grid_layout = QGridLayout()
            self.grid_layouts[tab.objectName()] = (grid_layout, search_bar)

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


    def update(self):
        self.clear_tables()
        self.create_tables(
            self.mineral_system_selection.currentText().lower(), self.scale_selection.currentText().lower()
        )


    def create_tables(self, mineral_system: str, scale: str):
        """Create new tables for each tab with selected mineral system and scale."""
        with open(os.path.join(PLUGIN_PATH, "resources/proxies.json"), "r") as f:
            proxy_data = json.loads(f.read())

        # Process each tab one by one
        for tab in self.tab_widgets:
            tab_name = tab.objectName()
            category = tab_name.split("_")[0]
            grid_layout, _ = self.grid_layouts[tab_name]
            proxies = proxy_data[mineral_system][category]

            # Sort proxies
            sorted_proxies = dict(
                sorted(
                    proxies.items(),
                    key=lambda proxy: IMPORTANCE_VALUES[proxy[1]["importance"][scale]]
                    )
                )

            # Create label row
            self.create_table_row(grid_layout, 0, "Proxy", "Importance", ["Keywords"], label=True)

            # Create rows for the table
            for i, (proxy_name, proxy_details) in enumerate(sorted_proxies.items()):
                i = i + 1  # Skip first row
                self.create_table_row(
                    grid_layout=grid_layout,
                    row=i,
                    name=proxy_name,
                    importance=proxy_details["importance"][scale],
                    keywords=proxy_details["keywords"],
                )


    def create_table_row(
        self,
        grid_layout: QGridLayout,
        row: int,
        name: str,
        importance: str,
        keywords: List[str],
        label=False,
    ):
        """Create a new row in the proxy table."""
        # 0. Importance
        importance_label = QLabel("*")
        if importance != "Importance":
            if IMPORTANCE_VALUES[importance] == 1:
                importance_label.setStyleSheet("color: red;")
                importance_label.setToolTip("Importance: High")
            elif IMPORTANCE_VALUES[importance] == 2:
                importance_label.setStyleSheet("color: orange;")
                importance_label.setToolTip("Importance: Moderate")
            elif IMPORTANCE_VALUES[importance] == 3:
                importance_label.setStyleSheet("color: green;")
                importance_label.setToolTip("Importance: Low")
            grid_layout.addWidget(importance_label, row, 0)

        # 1. Name label
        name_label = QLabel(name)
        name_label.setWordWrap(True)
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        grid_layout.addWidget(name_label, row, 1)

        # 2. Keywords label
        if COLOR_CODE_KEYWORDS:
            keywords_label = QLabel()
            colors = {
                "geology": "sandybrown",
                "geophysics": "blue",
                "geochemistry": "orange",
            }
            keywords_text = ""

            for word in keywords:
                if word in colors.keys():
                    keywords_text += (
                        f"<span style='color: {colors[word]};'>{word}</span>, "
                    )
                else:
                    keywords_text += f"{word}, "
            keywords_text = keywords_text[:-2]
            keywords_label.setText("<html><body>" + keywords_text + "</body></html>")
        else:
            keywords_label = QLabel(", ".join(keywords))
        keywords_label.setWordWrap(True)
        grid_layout.addWidget(keywords_label, row, 2)

        if label:
            name_label.setFont(self.bold_font)
            keywords_label.setFont(self.bold_font)
        else:
            # 3. Process button
            process_button = QPushButton("Process")
            process_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            process_button.clicked.connect(lambda: self.open_proxy_creation(name_label.text()))
            grid_layout.addWidget(process_button, row, 3)

            self.proxy_info[name] = (keywords, [name_label, importance_label, keywords_label, process_button])


    def update_table(self, search_text: str):
        """Updates proxy table based on search."""
        for proxy_name, (keywords, widgets) in self.proxy_info.items():
            if (
                search_text.lower() in proxy_name.lower()
                or any(search_text.lower() in word.lower() for word in keywords)
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
