import numpy as np
from qgis.core import QgsMapLayer
from qgis.gui import QgsMapLayerComboBox, QgsFieldComboBox, QgsColorButton, QgsOpacityWidget
from qgis.PyQt.QtWidgets import (
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QWidget
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

from eis_qgis_plugin import pyqtgraph as pg
from .plot_utils import update_color_selection, create_brush, create_pen, opacity_to_alpha, CHART_MAPPINGS, ChartType

FORM_CLASS: QWidget = load_ui("explore/basic_charts_tab.ui")


### TEST DATA
chi_data = np.random.chisquare(2, 100)
normal_data = np.random.normal(size = 100, loc =0)
x_data = np.arange(-50, 50)
line_test_data_1 = x_data, normal_data
line_test_data_2 = x_data, chi_data

SCATTER_TEST_DATA = [np.random.normal(size=(2, 1000)), 
                     np.random.normal(size=(2, 500), loc = 4)]
LINE_TEST_DATA = [line_test_data_1, line_test_data_2]
BAR_TEST_DATA = line_test_data_1
BOX_TEST_DATA = normal_data, chi_data

chi_data_1000 = np.random.chisquare(2, 1000)
normal_data_1000 = np.random.normal(size = 1000, loc=5)
x_data_1000 = np.arange(1000)
HISTOGRAM_TEST_DATA = np.array([chi_data_1000, normal_data_1000])



class BasicCharts(QWidget, FORM_CLASS):

    # Plot parameters
    layer_selection: QgsMapLayerComboBox
    chart_selection: QComboBox
    x_data_selection: QgsFieldComboBox
    y_data_selection: QgsFieldComboBox

    # Plot style parameters
    color_selection: QgsColorButton
    marker_type_selection: QComboBox
    line_type_selection: QComboBox
    opacity_selection: QgsOpacityWidget

    # Other widgets
    plot_container: QWidget
    plot_button: QPushButton
    clear_button: QPushButton


    def __init__(self):
        # Initialize
        super().__init__()
        self.setupUi(self)
        self.init_basic_charts()

        self.plot_number = 0

        # Connect signals
        self.layer_selection.layerChanged.connect(self.update_plot_parameters)
        self.plot_button.clicked.connect(self.plot)
        self.clear_button.clicked.connect(self.clear_plots)

        # Populate widgets
        self.update_plot_parameters(self.layer_selection.currentLayer())
        update_color_selection(self.color_selection, self.plot_number)


    def init_basic_charts(self):
        self.plot_widget = pg.PlotWidget(parent=self.plot_container)
        self.plot_widget.setMinimumSize(450, 430)
        self.styles = {"color": "r", "font-size": "14px"}
        self.plot_widget.setLabel("left", "Y label", **self.styles)
        self.plot_widget.setLabel("bottom", "X label", **self.styles)
        self.plot_widget.addLegend()
        self.plot_widget.setBackground("w")
        self.plot_widget.setTitle("Chart title")

        self.plot_layout = QVBoxLayout(self.plot_container)
        self.plot_layout.addWidget(self.plot_widget)


    def update_plot_parameters(self, layer: QgsMapLayer) -> None:
        if layer is not None:
            self.x_data_selection.setLayer(layer)
            self.y_data_selection.setLayer(layer)


    def clear_plots(self):
        """Called when clear_button is clicked.

        Clears all plots currently in the plot widget."""
        self.plot_widget.clear()
        self.plot_number = 0
        update_color_selection(self.color_selection, self.plot_number)


    def get_field_data(self, layer, field_name):
        return [feature[field_name] for feature in layer.getFeatures()]


    def plot(self):
        """Called when plot_button is clicked.

        Calls a plot creation function based on chart type selection."""
        chart_type = CHART_MAPPINGS[self.chart_selection.currentText().lower()]

        if chart_type == ChartType.SCATTER:
            # print(SCATTER_TEST_DATA[self.plot_number])
            layer = self.layer_selection.currentLayer()

            x_field = self.x_data_selection.currentField()
            x_field_data = self.get_field_data(layer, x_field)
            
            y_field = self.y_data_selection.currentField()
            y_field_data = self.get_field_data(layer, y_field)

            data = np.array([x_field_data, y_field_data])
            self.plot_scatterplot(data)

            self.plot_widget.setLabel("left", y_field, **self.styles)
            self.plot_widget.setLabel("bottom", x_field, **self.styles)
            
            self.plot_number += 1

        elif chart_type == ChartType.LINE:
            self.plot_line_plot(LINE_TEST_DATA[self.plot_number])
            self.plot_number += 1

        elif chart_type == ChartType.BAR:
            self.plot_bar_plot(BAR_TEST_DATA)
            self.plot_number += 1

        elif chart_type == ChartType.HISTOGRAM:
            self.plot_histogram(HISTOGRAM_TEST_DATA)
            self.plot_number += 1

        else:
            print("Not implemented yet")

        update_color_selection(self.color_selection, self.plot_number)


    def plot_scatterplot(self, data):
        brush = create_brush(self.color_selection, opacity_to_alpha(self.opacity_selection.opacity()))
        scatterplot = pg.ScatterPlotItem(size=8, brush=brush)
        pos = [{'pos': data[:, i]} for i in range(data.shape[1])]
        scatterplot.setData(pos)
        self.plot_widget.addItem(scatterplot)


    def plot_line_plot(self, data):
        pen = create_pen(self.color_selection, opacity_to_alpha(self.opacity_selection.opacity()))
        data_x = data[0]
        data_y = data[1]
        self.plot_widget.plot(
            data_x, data_y, name=f"Dataset {self.plot_number}", pen=pen
        )


    def plot_bar_plot(self, data):
        brush = create_brush(self.color_selection, opacity_to_alpha(self.opacity_selection.opacity()))
        bargraph = pg.BarGraphItem(x = data[0], height = data[1], width = 0.5, brush = brush)
        self.plot_widget.addItem(bargraph)


    def plot_histogram(self, data):
        brush = create_brush(self.color_selection, opacity_to_alpha(self.opacity_selection.opacity()))
        hist, bins = np.histogram(data)
        self.plot_widget.plot(
            bins,
            hist,
            name=f"Dataset {self.plot_number}",
            stepMode=True,
            fillLevel=0,
            brush=brush
        )
