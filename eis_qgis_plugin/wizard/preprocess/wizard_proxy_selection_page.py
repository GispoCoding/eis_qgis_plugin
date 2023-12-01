import json
import os

from pathlib import Path
from typing import Dict, List, Tuple

from qgis.PyQt import QtGui
from qgis.PyQt.QtWidgets import (
    QWizardPage,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QCheckBox,
)

from qgis.core import (
    QgsVectorLayer,
    QgsProject,
    QgsLayerTreeModel,
)

from qgis.gui import (
    QgsMapLayerComboBox,
    QgsFieldComboBox,
    QgsFieldExpressionWidget,
    QgsFileWidget,
    QgsLayerTreeView,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui


FORM_CLASS: QWizardPage = load_ui("preprocess/wizard_proxy_selection.ui")
path = Path(os.path.dirname(__file__)).parent.parent


COLOR_CODE_IMPORTANCE = True
COLOR_CODE_KEYWORDS = True


class EISWizardProxySelection(QWizardPage, FORM_CLASS):
    layer_selection: QgsMapLayerComboBox
    attribute_selection: QgsFieldComboBox
    field_expression: QgsFieldExpressionWidget

    output_file: QgsFileWidget

    def __init__(self, scale, mineral_system) -> None:
        super().__init__()
        self.setupUi(self)

        self.proxy_widgets: Dict[str, Tuple[str, list, QWidget]] = {}

        self.bold_font = QtGui.QFont()
        self.bold_font.setBold(True)

        self.init_proxies(mineral_system.lower(), scale.lower())

        # Repaint
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
                    grid_layout, 0, "Proxy", "Importance", ["Keywords"], label=True
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

        # 1. Name label
        name_label = QLabel(name)
        name_label.setWordWrap(True)
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        grid_layout.addWidget(name_label, row, 0)

        # 2. Importance label
        importance_label = QLabel(importance)
        if COLOR_CODE_IMPORTANCE and importance_label.text() != "Importance":
            if self.importance_value(importance_label.text()) == 1:
                importance_label.setStyleSheet("color: red;")
            elif self.importance_value(importance_label.text()) == 2:
                importance_label.setStyleSheet("color: orange;")
            elif self.importance_value(importance_label.text()) == 3:
                importance_label.setStyleSheet("color: green;")
        grid_layout.addWidget(importance_label, row, 1)

        # 3. Keywords label
        if COLOR_CODE_KEYWORDS:
            keywords_label = QLabel()
            colors = {
                "geology": "sandybrown",
                "geophysics": "blue",
                "geochemistry": "orange",
                #   "lithology": "darkblue",
                #   "mineralogy": "brown"
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
            checkbox_label = QLabel("Done")
            grid_layout.addWidget(checkbox_label, row, 3)

            name_label.setFont(self.bold_font)
            importance_label.setFont(self.bold_font)
            keywords_label.setFont(self.bold_font)
            checkbox_label.setFont(self.bold_font)

        else:
            # 4. "Done" checkbox
            checkbox = QCheckBox()
            checkbox.setText("")
            grid_layout.addWidget(checkbox, row, 3)

            # 5. Process button
            process_button = QPushButton("Process")
            process_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            grid_layout.addWidget(process_button, row, 4)

            # process_button.clicked.connect(lambda: self.open_proxy_creation(name_label.text()))
            process_button.clicked.connect(lambda: self.create_and_update_tree_view(row, name, grid_layout))

            # 6. Load button
            load_button = QPushButton("Load")
            load_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            grid_layout.addWidget(load_button, row, 5)

            self.proxy_widgets[name] = (
                importance,
                keywords,
                name_label,
                importance_label,
                keywords_label,
                checkbox,
                process_button,
                load_button,
                None, # Placeholder for tree view
            )

    def update_widgets(self, text):
        for proxy, (
            importance,
            keywords,
            name_label,
            importance_label,
            keywords_label,
            checkbox,
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
                checkbox.show()
                process_button.show()
                load_button.show()
            else:
                name_label.hide()
                importance_label.hide()
                keywords_label.hide()
                checkbox.hide()
                process_button.hide()
                load_button.hide()

    # def open_proxy_creation(self, proxy_name):
    #     self.wizard().page2.selected_proxy_label.setText(proxy_name)
    #     self.wizard().next()

    def create_and_update_tree_view(self, row, name, grid_layout):
        # Retrieve the existing widgets for the row
        (
            importance,
            keywords,
            name_label,
            importance_label,
            keywords_label,
            checkbox,
            process_button,
            load_button,
            tree_view,
        ) = self.proxy_widgets[name]

        vector_layer = QgsVectorLayer("Point?crs=EPSG:4326", f"my_vector_layer_{row}", "memory")

        if tree_view is None:
            # Create a new child grid layout for the row
            child_grid_layout = QGridLayout()
            grid_layout.addLayout(child_grid_layout, row + 1, 0, 1, grid_layout.columnCount())

            # Create QgsLayerTreeView and add it to the child grid layout
            tree_view = QgsLayerTreeView()
            child_grid_layout.addWidget(tree_view, 0, 0, 1, child_grid_layout.columnCount())

            # Create QgsLayerTreeModel
            layer_tree_model = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot())

            # Connect the model to the view
            tree_view.setModel(layer_tree_model)

            # Store the tree view in the dictionary
            self.proxy_widgets[name] = (
                importance,
                keywords,
                name_label,
                importance_label,
                keywords_label,
                checkbox,
                process_button,
                load_button,
                tree_view,
            )

            if vector_layer.isValid():
                root_group = layer_tree_model.rootGroup()
                root_group.addLayer(vector_layer)

        else:
            if vector_layer.isValid():
                layer_tree_model = tree_view.layerTreeModel()
                root_group = layer_tree_model.rootGroup()
                root_group.addLayer(vector_layer)

        # TODO: TreeView currently isn't updated. Why?
