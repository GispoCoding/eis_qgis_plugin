import numpy as np
from qgis.PyQt.QtWidgets import QDialog, QTabWidget, QVBoxLayout, QWidget
from qgis.utils import iface

from eis_qgis_plugin import pyqtgraph as pg
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

from .basic_plots_pyqtgraph import BasicCharts
from .parallel_coordinates_plot import ParallelChart

FORM_CLASS: QDialog = load_ui("explore/wizard_explore_window.ui")


class EISWizardExplore(QDialog, FORM_CLASS):
    tab_widget: QTabWidget

    container: QWidget

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.iface = iface

        self.basic_charts_tab = BasicCharts()
        self.parallel_charts_tab = ParallelChart()

        self.tab_widget.addTab(self.basic_charts_tab, "Basic charts")
        self.tab_widget.addTab(self.parallel_charts_tab, "Parallel coordinates")

        self.create_roi()

    def create_roi(self):
        self.plot_widget_roi = pg.PlotWidget(parent=self.container)
        roi = pg.ROI([10, 10], [10, 10])
        self.plot_widget_roi.addItem(roi)

        self.plot_widget_roi.setMinimumSize(450, 430)
        self.styles = {"color": "r", "font-size": "14px"}
        self.plot_widget_roi.setLabel("left", "Y label", **self.styles)
        self.plot_widget_roi.setLabel("bottom", "X label", **self.styles)
        self.plot_widget_roi.addLegend()
        self.plot_widget_roi.setBackground("w")
        self.plot_widget_roi.setTitle("Chart title")

        self.plot_layout = QVBoxLayout(self.container)
        self.plot_layout.addWidget(self.plot_widget_roi)

    def plot_boxplot(self, data):
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


class EISWizardExploreBig(
    QDialog, load_ui("old_designs_and_tests/wizard_explore_big_plotly_test.ui")
):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.iface = iface


# def plot_3D_scatterplot(self, data):
#     # NOTE: Need to use GlViewWidget, maybe better to have 3D in another tab?
#     # Create 3D scatter plot data
#     n = 1000
#     x = np.random.normal(size=n)
#     y = np.random.normal(size=n)
#     z = np.random.normal(size=n)

#     # Create the GLScatterPlotItem
#     scatterplot = gl.GLScatterPlotItem(pos=np.vstack([x,y,z]).T, size=8, pxMode=True)
#     self.plot_widget.addItem(scatterplot)
