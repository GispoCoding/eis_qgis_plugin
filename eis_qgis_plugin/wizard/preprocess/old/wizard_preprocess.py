import json
import os

from pathlib import Path
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
    QDialog
)

from qgis.gui import (
    QgsMapLayerComboBox,
    QgsFieldComboBox,
    QgsFieldExpressionWidget,
    QgsFileWidget
)



from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from ..preprocess.create_proxy import EISWizardProxy

FORM_CLASS: QDialog = load_ui("preprocess/wizard_preprocess_iocg.ui")
# FORM_CLASS: QWizard = load_ui("preprocess/wizard_preprocess_iocg_3.ui")
path = Path(os.path.dirname(__file__)).parent.parent


class EISWizardPreprocess(QDialog, FORM_CLASS):
    layer_selection: QgsMapLayerComboBox
    attribute_selection: QgsFieldComboBox
    field_expression: QgsFieldExpressionWidget

    output_file: QgsFileWidget

    def __init__(self, scale, mineral_system) -> None:
        super().__init__()
        self.setupUi(self)

        # PAGE 1
        self.proxy_widgets: Dict[str, Tuple[str, list, QWidget]] = {}

        self.bold_font = QtGui.QFont()
        self.bold_font.setBold(True)

        self.init_proxies(mineral_system, scale)

        # Repaint
        self.source_tab.repaint()
        self.pathway_tab.repaint()
        self.depositional_tab.repaint()
        self.mineralisation_tab.repaint()

        # self.open_explore_btn.clicked.connect(self.open_explore)

        # # PAGE 2
        # self.selected_layer: QgsVectorLayer = None
        # self.selected_field: QgsField = None
        # self.layer_selection.setFilters(QgsMapLayerProxyModel.VectorLayer)
        # self.layer_selection.layerChanged.connect(self.set_layer)
        # self.attribute_selection.fieldChanged.connect(self.set_field)
        
        # # Connect buttons
        # self.compute_and_plot_btn.clicked.connect(self.compute_and_plot)
        # self.select_data_btn.clicked.connect(self.select_data)
        # self.create_file_btn.clicked.connect(self.create_file_from_selection)
        # self.idw_btn.clicked.connect(lambda _: processing.execAlgorithmDialog("eis:simple_idw", {}) )
        # self.kriging_btn.clicked.connect(lambda _: processing.execAlgorithmDialog("eis:kriging_interpolation", {}) )
        # self.distance_raster_btn.clicked.connect(
        #     lambda _: processing.execAlgorithmDialog("eis:distance_computation", {})
        # )

        # # Set plot layout
        # self.plot_layout = QVBoxLayout()
        # self.plot_widget.setLayout(self.plot_layout)


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
            process_button.clicked.connect(self.open_proxy_creation)
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


    def open_proxy_creation(self):
        self.proxy_window = EISWizardProxy(self)
        self.proxy_window.show()


    # def open_explore(self):
    #     self.explore_window = EISWizardExplore(self)
    #     self.explore_window.show()

    # ----- PAGE 2 -----

    # def set_layer(self, layer):
    #     self.attribute_selection.setLayer(layer)
    #     self.selected_layer = layer
    #     self.set_field(self.attribute_selection.currentField())

    # def set_field(self, field_name):
    #     self.selected_field = field_name
    #     self.field_expression.setField(field_name)

    # def compute_and_plot(self):
    #     if self.selected_layer is None or self.selected_field is None:
    #         print("Select a layer and field first!")
    #     else:
    #         self.get_statistics()
    #         self.plot_distribution()  

    # def select_data(self):
    #     if self.field_expression.isValidExpression():
    #         self.selected_layer.selectByExpression(self.field_expression.expression(), QgsVectorLayer.SetSelection)
    #     else:
    #         print("Expression invalid!")

    # def create_file_from_selection(self):
    #     print(self.output_file.filePath())
    #     self.output_file.set

    # def get_statistics(self):
    #     # my_result = processing.run("eis:descriptive_statistics",
    #     #     {
    #     #         'input_layer': '/data/lines.shp',
    #     #         'output_file': '/data/buffers.shp'
    #     #     }
    #     # )
    #     # output = my_result['OUTPUT']
    #     self.max_output.setText("1")
    #     self.min_output.setText("2")
    #     self.mean_output.setText("3")
    #     self.median_output.setText("4")

    # def plot_distribution(self):
    #     for i in reversed(range(self.plot_layout.count())):
    #         widget = self.plot_layout.itemAt(i).widget()
    #         if widget is not None:
    #             widget.deleteLater()

    #     # Create Seaborn plot
    #     values = [feature.attribute(self.selected_field) for feature in self.selected_layer.getFeatures()]
    #     values_no_null = [value for value in values if value != NULL]

    #     fig, ax = plt.subplots()
    #     sns.histplot(data=values_no_null, ax=ax)
    #     canvas = FigureCanvas(fig)
    #     canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    #     toolbar = NavigationToolbar(canvas, self.plot_widget)

    #     # # Create Seaborn plot
    #     # penguins = sns.load_dataset("penguins")
    #     # fig, ax = plt.subplots()
    #     # sns.histplot(data=penguins, x="flipper_length_mm", ax=ax)
    #     # canvas = FigureCanvas(fig)
    #     # canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    #     self.plot_layout.addWidget(toolbar)
    #     self.plot_layout.addWidget(canvas)


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
