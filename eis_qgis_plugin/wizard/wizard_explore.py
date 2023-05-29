import numpy as np
from qgis.core import QgsMapLayer
from qgis.gui import QgisInterface
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QDialog
from qgis.utils import iface

from eis_qgis_plugin import pyqtgraph as pg
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QDialog = load_ui("wizard_explore_window2.ui")


class EISWizardExplore(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.iface = iface

        self.plot_widget = pg.PlotWidget(parent=self.plot_container)
        self.plot_widget.setMinimumSize(450, 430)
        styles = {"color": "r", "font-size": "14px"}
        self.plot_widget.setLabel("left", "Y label", **styles)
        self.plot_widget.setLabel("bottom", "X label", **styles)
        self.plot_widget.addLegend()
        self.plot_widget.setBackground("w")
        self.plot_widget.setTitle("Chart title")

        self.plot_layout = QtWidgets.QVBoxLayout(self.plot_container)
        self.plot_layout.addWidget(self.plot_widget)

        self.layer_selection.layerChanged.connect(self.update_plot_parameters)
        self.chart_selection.currentIndexChanged.connect(self.update_chart_type)
        self.plot_button.clicked.connect(self.plot)

        self.update_plot_parameters(self.layer_selection.currentLayer())
        self.update_chart_type(self.chart_selection.currentIndex())

    def update_plot_parameters(self, layer: QgsMapLayer) -> None:
        self.single_plot_layer = layer
        if layer is not None:
            self.x_data_selection.setLayer(layer)
            self.y_data_selection.setLayer(layer)
            self.z_data_selection.setLayer(layer)

    def update_chart_type(self, i):
        if self.chart_selection.currentText().lower() == "3d scatter plot":
            self.z_data_selection.show()
            self.z_label.show()
        else:
            self.z_data_selection.hide()
            self.z_label.hide()

    def plot(self):
        self.plot_widget.clear()

        chart_type = self.chart_selection.currentText().lower()
        if chart_type == "line plot":
            data1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [
                0,
                1,
                2,
                3.5,
                4,
                5,
                5.5,
                4,
                3,
                1.5,
            ]
            data2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [
                1,
                2,
                5,
                7,
                7.5,
                9.3,
                6.5,
                3.5,
                4.0,
                5.5,
            ]
            data = (data1, data2)
            self.create_line_plot(data)
        elif chart_type == "box plot":
            data = [
                np.random.normal(size=100, loc=0),
                np.random.normal(size=100, loc=1),
            ]
            self.create_boxplot(data)
        elif chart_type == "histogram":
            # data = np.array([[1, 1, 2, 3, 4, 5, 5, 5, 5, 4, 3, 10],
            # [2, 3, 4, 4, 1, 10, 9, 9, 5, 4, 3, 10]])
            # x1 = np.random.normal(0, 0.8, 1000)
            # x2 = np.random.normal(-2, 1, 1000)
            # x3 = np.random.normal(3, 2, 1000)
            data = np.array(
                [
                    [
                        [1, 1, 2, 3, 4, 5, 5, 5, 5, 4, 3, 10],
                        [2, 3, 4, 4, 1, 10, 9, 9, 5, 4, 3, 10],
                    ],
                    [
                        [11, 13, 14, 14, 4, 5, 9, 5, 9, 4, 3, 10],
                        [4, 4, 4, 9, 11, 10, 9, 9, 5, 4, 3, 10],
                    ],
                ]
            )
            self.create_histogram(data)
        else:
            print("Not implemented yet")

    def create_histogram(self, data):
        brushes = [
            pg.mkBrush(color=(25, 132, 197, 150), width=3),
            pg.mkBrush(color=(208, 238, 17, 150), width=3),
        ]
        # Plot multiple bands
        if data.ndim == 3:
            for i, data_2d in enumerate(data):
                data_1d = data_2d.ravel()
                if i == 0:
                    hist, bins = np.histogram(data_1d)
                else:
                    hist, bins = np.histogram(data_1d, bins=bins)
                self.plot_widget.plot(
                    bins,
                    hist,
                    name=f"Dataset {i}",
                    stepMode=True,
                    fillLevel=0,
                    brush=brushes[i],
                )

        # Plot one band
        else:
            data_1d = data_2d.ravel()
            hist, bins = np.histogram(data_1d)
            self.plot_widget.plot(
                bins, hist, stepMode=True, fillLevel=0, brush=(0, 0, 255, 150)
            )

    def create_boxplot(self, data):
        for i, dataset in enumerate(data):
            for item in self.create_box(dataset, i):
                self.plot_widget.addItem(item)

    def create_box(self, data, position):
        # Data for box
        quartile1 = np.percentile(data, 25)
        quartile3 = np.percentile(data, 75)
        med = np.median(data)
        iqr = quartile3 - quartile1
        whisker = 1.5 * iqr

        # Exclude data beyond whiskers
        data = data[(data > quartile1 - whisker) & (data < quartile3 + whisker)]

        width = 0.3

        # Generate box
        box = pg.ErrorBarItem(
            x=np.array([position]),
            y=np.array([med]),
            height=np.array([quartile3 - quartile1]),
            width=width,
            brush=(0, 0, 0, 30),
        )
        whisker_top = pg.ErrorBarItem(
            x=np.array([position]),
            y=np.array([quartile3]),
            height=np.array([quartile3 - data.max()]),
            width=width,
            pen=(255, 0, 0),
        )
        whisker_bottom = pg.ErrorBarItem(
            x=np.array([position]),
            y=np.array([quartile1]),
            height=np.array([data.min() - quartile1]),
            width=width,
            pen=(255, 0, 0),
        )

        # Draw scatter points for all data
        scatter = pg.ScatterPlotItem(
            x=np.full(data.shape, position),
            y=data,
            pen=(0, 0, 50),
            brush=(0, 0, 0),
            size=5,
        )

        return [box, whisker_top, whisker_bottom, scatter]

    def create_line_plot(self, data):
        # Add some random data to the plot. Replace this with your actual data.
        pens = [
            pg.mkPen(color=(25, 132, 197), width=3),
            pg.mkPen(color=(208, 238, 17), width=3),
        ]
        for i, dataset in enumerate(data):
            dataset_x = dataset[0]
            dataset_y = dataset[1]
            self.plot_widget.plot(
                dataset_x, dataset_y, name=f"Dataset {i}", pen=pens[i]
            )


class EISWizardExploreBig(QtWidgets.QDialog, load_ui("wizard_explore_big.ui")):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.iface = iface
