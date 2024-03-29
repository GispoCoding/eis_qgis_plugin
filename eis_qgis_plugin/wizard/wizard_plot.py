import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from qgis.PyQt.QtWidgets import QComboBox, QFrame, QPushButton, QSizePolicy, QStackedWidget, QVBoxLayout, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.plots.barplot import EISWizardBarplot
from eis_qgis_plugin.wizard.plots.boxplot import EISWizardBoxplot
from eis_qgis_plugin.wizard.plots.ecdf import EISWizardEcdf
from eis_qgis_plugin.wizard.plots.histogram import EISWizardHistogram
from eis_qgis_plugin.wizard.plots.kde import EISWizardKde
from eis_qgis_plugin.wizard.plots.lineplot import EISWizardLineplot
from eis_qgis_plugin.wizard.plots.pairplot import EISWizardPairplot
from eis_qgis_plugin.wizard.plots.parallel_coordinates import EISWizardParallelCoordinatesPlot
from eis_qgis_plugin.wizard.plots.scatterplot import EISWizardScatterplot

FORM_CLASS: QWidget = load_ui("explore/wizard_plot.ui")



class EISWizardPlotting(QWidget, FORM_CLASS):

    plot_type_selection: QComboBox
    plot_container: QFrame
    plot_parameters_container: QStackedWidget

    create_plot_btn: QPushButton
    open_plot_btn: QPushButton
    clear_plot_btn: QPushButton
    reset_btn: QPushButton


    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.latest_figure = None

        # Initialize buttons
        self.create_plot_btn.clicked.connect(self.create_plot)
        self.open_plot_btn.clicked.connect(self.open_plot)
        self.clear_plot_btn.clicked.connect(self.close_and_remove_plot)
        self.reset_btn.clicked.connect(self.reset_parameters)

        self.plot_type_selection.currentIndexChanged['int'].connect(self.plot_parameters_container.setCurrentIndex)

        self.plot_parameters_container.currentChanged.connect(self.resize_parameter_container)

        # Create pages for parameters
        self.pages = [
            EISWizardHistogram(self),
            EISWizardKde(self),
            EISWizardEcdf(self),
            EISWizardScatterplot(self),
            EISWizardLineplot(self),
            EISWizardBarplot(self),
            EISWizardBoxplot(self),
            EISWizardPairplot(self),
            EISWizardParallelCoordinatesPlot(self)
        ]

        for i, page in enumerate(self.pages):
            self.plot_parameters_container.insertWidget(i, page)

        # Init plot space
        self.plot_layout = QVBoxLayout()
        self.plot_container.setLayout(self.plot_layout)


    def resize_parameter_container(self, index):
        """Resize the QStackedWidget that contains plot parameters according to the needed size."""
        widget = self.plot_parameters_container.widget(index)
        if widget:
            self.plot_parameters_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.plot_parameters_container.setMinimumHeight(widget.height())


    def create_plot(self):
        self.close_and_remove_plot()

        page = self.pages[self.plot_parameters_container.currentIndex()]

        fig, ax = plt.subplots()
        if isinstance(page, EISWizardPairplot):
            fig = page.plot(ax)
        elif isinstance(page, EISWizardParallelCoordinatesPlot):
            page.plot(ax, fig)
        else:
            page.plot(ax)

        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar = NavigationToolbar(canvas, self.plot_container)

        self.plot_layout.addWidget(toolbar)
        self.plot_layout.addWidget(canvas)


    def open_plot(self):
        plt.show()


    def close_and_remove_plot(self):
        plt.close('all')
        for i in reversed(range(self.plot_layout.count())):
            widget = self.plot_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()


    def reset_parameters(self):
        self.pages[self.plot_parameters_container.currentIndex()].reset()



    ## STATS

    # def compute_statistics(self):
    #     # Get N
    #     layer = self.data_summary_layer_selection.currentLayer()
    #     if (
    #         layer.type() == QgsMapLayer.VectorLayer
    #     ):  # NOTE: Same snippet later, refactor at some point
    #         field = self.data_summary_field_selection.currentField()
    #         all_values = [feature.attribute(field) for feature in layer.getFeatures()]
    #         nr_of_all_values = len(all_values)
    #         nr_of_nulls = len([value for value in all_values if value == NULL])
    #         nr_of_valids = nr_of_all_values - nr_of_nulls

    #     elif (
    #         layer.type() == QgsMapLayer.RasterLayer
    #     ):  # NOTE: Same snippet later, refactor at some point
    #         data_provider = layer.dataProvider()
    #         width = layer.width()
    #         height = layer.height()
    #         band = int(self.data_summary_band_selection.currentIndex())

    #         data_block = data_provider.block(band, layer.extent(), width, height)
    #         nr_of_nulls = 0
    #         nr_of_valids = 0
    #         nr_of_all_values = width * height

    #         # Loop over all pixels
    #         for row in range(height):
    #             for col in range(width):
    #                 pixel_value = data_block.value(row, col)
    #                 if pixel_value == NULL:
    #                     nr_of_nulls += 1
    #                 else:
    #                     nr_of_valids += 1

    #     else:
    #         raise Exception("Not vector or raster")

    #     self.n_total.setText(str(nr_of_all_values))
    #     self.n_null.setText(str(nr_of_nulls))
    #     self.n_valid.setText(str(nr_of_valids))

    #     # Get descriptive statistics

    #     if layer.type() == QgsMapLayer.VectorLayer:
    #         descriptive_statistics_results = processing.run(
    #             "eis:descriptive_statistics_vector",
    #             {
    #                 "input_file": self.data_summary_layer_selection.currentLayer(),
    #                 "column": self.data_summary_field_selection.currentField(),
    #             },
    #         )
    #     else:
    #         descriptive_statistics_results = processing.run(
    #             "eis:descriptive_statistics_raster",
    #             {
    #                 "input_file": self.data_summary_layer_selection.currentLayer(),
    #             },
    #         )

    #     self.min.setText(str(descriptive_statistics_results["min"]))
    #     self.quantile25.setText(str(descriptive_statistics_results["25%"]))
    #     self.median.setText(str(descriptive_statistics_results["50%"]))
    #     self.quantile75.setText(str(descriptive_statistics_results["75%"]))
    #     self.max.setText(str(descriptive_statistics_results["max"]))

    #     self.mean.setText(str(descriptive_statistics_results["mean"]))
    #     self.stdev.setText(str(descriptive_statistics_results["standard_deviation"]))
    #     self.relative_stdev.setText(
    #         str(descriptive_statistics_results["relative_standard_deviation"])
    #     )
    #     self.skewness.setText(str(descriptive_statistics_results["skew"]))
