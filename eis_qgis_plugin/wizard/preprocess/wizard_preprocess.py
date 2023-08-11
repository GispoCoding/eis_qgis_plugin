import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

from qgis.PyQt import QtGui
from qgis.PyQt.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QDialog = load_ui("preprocess/wizard_preprocess_iocg.ui")
path = Path(os.path.dirname(__file__)).parent.parent


class EISWizardPreprocess(QDialog, FORM_CLASS):
    def __init__(self, scale, mineral_system) -> None:
        super().__init__()
        self.setupUi(self)

        self.proxy_widgets: Dict[str, Tuple[str, list, QWidget]] = {}

        self.bold_font = QtGui.QFont()
        self.bold_font.setBold(True)

        # self.create_active_pathway()
        self.init_proxies(mineral_system, scale)

        # self.overview_tab.repaint()
        self.source_tab.repaint()
        self.pathway_tab.repaint()
        self.depositional_tab.repaint()
        self.mineralisation_tab.repaint()

    def importance_value(self, importance_str):
        if importance_str.lower() == "high":
            return 1
        elif importance_str.lower() == "moderate":
            return 2
        elif importance_str.lower() == "low":
            return 3
        elif importance_str == "-":
            return 4
        else:
            raise Exception(f"Unidentified importance value {importance_str}")

    def init_proxies(self, mineral_system: str, scale: str):
        # Read json
        with open(os.path.join(path, "resources/proxies.json"), "r") as f:
            data = json.loads(f.read())
            proxy_categories = ["source", "pathway", "depositional", "mineralisation"]

            for category in proxy_categories:
                grid_layout = QGridLayout()
                proxies = data[mineral_system][category]

                # Label row
                self.create_row(
                    grid_layout, 0, "Proxy name", "Importance", ["Keywords"], label=True
                )

                sorted_proxies = dict(
                    sorted(
                        proxies.items(),
                        key=lambda proxy: self.importance_value(
                            proxy[1]["importance"][scale]
                        ),
                    )
                )
                for i, (proxy_name, proxy_details) in enumerate(sorted_proxies.items()):
                    i = i + 1  # Skip first row
                    self.create_row(
                        grid_layout=grid_layout,
                        row=i,
                        name=proxy_name,
                        importance=proxy_details["importance"][scale],
                        keywords=proxy_details["keywords"],
                    )

                # Crete main layout, add search layout and proxy layout
                self.main_layout = QVBoxLayout()

                self.search_layout = QHBoxLayout()
                self.search_label = QLabel("Search")
                self.search_bar = QLineEdit()
                self.search_bar.textChanged.connect(self.update_widgets)
                self.search_layout.addWidget(self.search_label)
                self.search_layout.addWidget(self.search_bar)
                self.main_layout.addLayout(self.search_layout)

                scroll_widget = QWidget()
                scroll_layout = QVBoxLayout()
                scroll_layout.addLayout(grid_layout)
                scroll_layout.addStretch()
                scroll_widget.setLayout(scroll_layout)
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                scroll_area.setWidget(scroll_widget)
                self.main_layout.addWidget(scroll_area)

                # Set the main layout
                tab: QWidget = getattr(self, category + "_tab")
                tab.setLayout(self.main_layout)

    def create_row(
        self,
        grid_layout: QGridLayout,
        row: int,
        name: str,
        importance: str,
        keywords: List[str],
        label=False,
    ):
        # Name label
        name_label = QLabel(name)
        name_label.setWordWrap(True)
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        grid_layout.addWidget(name_label, row, 0)

        # Importance label
        importance_label = QLabel(importance)
        grid_layout.addWidget(importance_label, row, 1)

        # Keywords label
        keywords_label = QLabel(", ".join(keywords))
        keywords_label.setWordWrap(True)
        grid_layout.addWidget(keywords_label, row, 2)

        if label:
            name_label.setFont(self.bold_font)
            importance_label.setFont(self.bold_font)
            keywords_label.setFont(self.bold_font)

        else:
            # Process button
            process_button = QPushButton("Process")
            process_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            grid_layout.addWidget(process_button, row, 3)

            # Load button
            load_button = QPushButton("Load")
            load_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            grid_layout.addWidget(load_button, row, 4)

            self.proxy_widgets[name] = (
                importance,
                keywords,
                name_label,
                importance_label,
                keywords_label,
                process_button,
                load_button,
            )

    def create_active_pathway(self):
        tab: QWidget = self.pathway_tab
        self.main_layout = QVBoxLayout()

        proxies: List[Tuple[str, str]] = [
            ("Major structures", "High"),
            ("Lower order structures", "High"),
            ("Fluid flow and deposition", "Moderate"),
            ("Proxy 4", "Low"),
            ("Something", "Low"),
        ]

        self.proxy_widgets: Dict[str, Tuple[str, QWidget]] = {}
        self.proxy_layout = QGridLayout()

        # Add header row
        bold_font = QtGui.QFont()
        bold_font.setBold(True)

        self.proxy_layout_header_widget = QWidget()
        self.proxy_layout_header_layout = QHBoxLayout()

        label = QLabel("Proxy")
        self.proxy_layout_header_layout.addWidget(label)
        label.setFont(bold_font)

        importance_label = QLabel("Importance")
        # importance_label.setMinimumWidth(82)
        self.proxy_layout_header_layout.addWidget(importance_label)
        importance_label.setFont(bold_font)

        process_label = QLabel("Process")
        self.proxy_layout_header_layout.addWidget(process_label)
        process_label.setFont(bold_font)

        load_label = QLabel("Load")
        self.proxy_layout_header_layout.addWidget(load_label)
        load_label.setFont(bold_font)

        self.proxy_layout_header_widget.setLayout(self.proxy_layout_header_layout)
        self.proxy_layout.addWidget(self.proxy_layout_header_widget, 0, 0, 1, 4)

        for i, (proxy, importance) in enumerate(proxies):
            i = i + 1
            proxy_widget = QWidget()
            proxy_layout = QHBoxLayout()

            proxy_label = QLabel(proxy)
            proxy_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            proxy_layout.addWidget(proxy_label)

            importance_label = QLabel(importance)
            importance_label.setMinimumWidth(82)
            proxy_layout.addWidget(importance_label)

            process_button = QPushButton("Process")
            process_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            proxy_layout.addWidget(process_button)

            load_button = QPushButton("Load")
            load_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            proxy_layout.addWidget(load_button)

            proxy_widget.setLayout(proxy_layout)

            self.proxy_widgets[proxy] = (importance, proxy_widget)
            self.proxy_layout.addWidget(proxy_widget, i, 0, 1, 4)

        self.search_layout = QHBoxLayout()
        self.search_label = QLabel("Search")
        self.search_bar = QLineEdit()
        self.search_bar.textChanged.connect(self.update_widgets)
        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_bar)
        self.main_layout.addLayout(self.search_layout)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.addLayout(self.proxy_layout)
        scroll_widget.setLayout(scroll_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        self.main_layout.addWidget(scroll_area)

        tab.setLayout(self.main_layout)

    def update_widgets(self, text):
        for proxy, (
            importance,
            keywords,
            name_label,
            importance_label,
            keywords_label,
            process_button,
            load_button,
        ) in self.proxy_widgets.items():
            if (
                text.lower() in proxy.lower()
                or text.lower() in importance.lower()
                or any(text.lower() in word.lower() for word in keywords)
            ):
                name_label.show()
                importance_label.show()
                keywords_label.show()
                process_button.show()
                load_button.show()
            else:
                name_label.hide()
                importance_label.hide()
                keywords_label.hide()
                process_button.hide()
                load_button.hide()

        # self.create_scroll_area()

    # def create_scroll_area(self):
    #     page = self.geoprocessing_3

    #     h_layout = QtWidgets.QHBoxLayout()
    #     scroll = QtWidgets.QScrollArea(page)
    #     scroll.setWidgetResizable(True) # CRITICAL

    #     inner = QtWidgets.QFrame(scroll)
    #     inner.setGeometry(QtCore.QRect(460, 80, 500, 500))

    #     layout = QtWidgets.QVBoxLayout()

    #     inner.setLayout(layout)
    #     scroll.setWidget(inner) # CRITICAL
    #     h_layout.addWidget(scroll)

    #     for i in range(10):

    #         # b = QtWidgets.QPushButton(inner)
    #         # b.setText(str(i))

    #         # b = self.create_group_box(i)

    #         b = QtWidgets.QGroupBox(inner)
    #         b.setTitle(f"AAA {i}")

    #         c = QtWidgets.QPushButton(b)
    #         c.setText(str(i))
    #         inner.layout().addWidget(b)
