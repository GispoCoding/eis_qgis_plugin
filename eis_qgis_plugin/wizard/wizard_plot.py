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
from eis_qgis_plugin.wizard.plots.scatterplot import EISWizardScatterplot

FORM_CLASS: QWidget = load_ui("wizard_plot.ui")



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
        self.histogram_page = EISWizardHistogram(self)
        self.kde_page = EISWizardKde(self)
        self.ecdf_page = EISWizardEcdf(self)
        self.scatterplot_page = EISWizardScatterplot(self)
        self.lineplot_page = EISWizardLineplot(self)
        self.barplot_page = EISWizardBarplot(self)
        self.boxplot_page = EISWizardBoxplot(self)
        self.pairplot_page = EISWizardPairplot(self)
        self.pages = [
            self.histogram_page,
            self.kde_page,
            self.ecdf_page,
            self.scatterplot_page,
            self.lineplot_page,
            self.barplot_page,
            self.boxplot_page,
            self.pairplot_page
        ]

        for i, page in enumerate(self.pages):
            self.plot_parameters_container.insertWidget(i, page)

        # Init plot space
        self.plot_layout = QVBoxLayout()
        self.plot_container.setLayout(self.plot_layout)


    def resize_parameter_container(self, index):
        widget = self.plot_parameters_container.widget(index)
        if widget:
            self.plot_parameters_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.plot_parameters_container.setMinimumHeight(widget.height())


    def on_close(self, event):
        print("Trying to intercept matplolib closing figure")


    def create_plot(self):
        self.close_and_remove_plot()

        # Tinker with matplolib
        # fig.canvas.mpl_connect('close_event', self.on_close)

        i = self.plot_parameters_container.currentIndex()
        page = self.pages[i]

        fig, ax = plt.subplots()
        if isinstance(page, EISWizardPairplot):
            fig = page.plot(ax)
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
        for i in reversed(range(self.plot_layout.count())):
            widget = self.plot_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()


    def reset_parameters(self):
        i = self.plot_parameters_container.currentIndex()
        self.pages[i].reset()
