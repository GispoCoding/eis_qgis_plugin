import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from qgis.core import QgsApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QComboBox, QDialogButtonBox, QFrame, QSizePolicy, QStackedWidget, QVBoxLayout, QWidget

from eis_qgis_plugin.eis_wizard.eda.plots.barplot import EISWizardBarplot
from eis_qgis_plugin.eis_wizard.eda.plots.boxplot import EISWizardBoxplot
from eis_qgis_plugin.eis_wizard.eda.plots.ecdf import EISWizardEcdf
from eis_qgis_plugin.eis_wizard.eda.plots.histogram import EISWizardHistogram
from eis_qgis_plugin.eis_wizard.eda.plots.kde import EISWizardKde
from eis_qgis_plugin.eis_wizard.eda.plots.lineplot import EISWizardLineplot
from eis_qgis_plugin.eis_wizard.eda.plots.pairplot_raster import EISWizardPairplotRaster
from eis_qgis_plugin.eis_wizard.eda.plots.pairplot_vector import EISWizardPairplotVector
from eis_qgis_plugin.eis_wizard.eda.plots.parallel_coordinates_raster import EISWizardParallelCoordinatesRasterPlot
from eis_qgis_plugin.eis_wizard.eda.plots.parallel_coordinates_vector import EISWizardParallelCoordinatesVectorPlot
from eis_qgis_plugin.eis_wizard.eda.plots.scatterplot import EISWizardScatterplot
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QWidget = load_ui("eda/wizard_plot.ui")



class EISWizardPlotting(QWidget, FORM_CLASS):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # DECLARE TYPES
        self.plot_type_selection: QComboBox
        self.plot_container: QFrame
        self.plot_parameters_container: QStackedWidget
        self.button_box: QDialogButtonBox

        self.latest_figure = None

        # Initialize buttons
        self.button_box.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.reset_parameters)
        self.button_box.button(QDialogButtonBox.RestoreDefaults).setAutoDefault(False)
        self.clear_plot_btn = self.button_box.addButton("Clear plot", QDialogButtonBox.ActionRole)
        self.clear_plot_btn.setIcon(QIcon(QgsApplication.getThemeIcon("mActionDeleteSelected.svg")))
        self.clear_plot_btn.clicked.connect(self.close_and_remove_plot)
        self.open_plot_btn = self.button_box.addButton("Open plot in a new window", QDialogButtonBox.ActionRole)
        self.open_plot_btn.setIcon(QIcon(QgsApplication.getThemeIcon("mActionZoomToLayer.svg")))
        self.open_plot_btn.clicked.connect(self.open_plot)
        self.create_plot_btn = self.button_box.addButton("Create plot", QDialogButtonBox.ActionRole)
        self.create_plot_btn.setIcon(QIcon(QgsApplication.getThemeIcon("mActionStart.svg")))
        self.create_plot_btn.clicked.connect(self.create_plot)
        self.create_plot_btn.setDefault(True)

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
            EISWizardPairplotVector(self),
            EISWizardPairplotRaster(self),
            EISWizardParallelCoordinatesVectorPlot(self),
            EISWizardParallelCoordinatesRasterPlot(self),
        ]

        for i, page in enumerate(self.pages):
            self.plot_parameters_container.insertWidget(i, page)

        # Init plot space
        self.plot_layout = QVBoxLayout()
        self.plot_container.setLayout(self.plot_layout)

        # TODO: Refactor
        for idx in (-1, -3):
            self.pages[idx].data_layer_table.size_changed.connect(
                lambda change: self.plot_parameters_container.setMinimumHeight(
                    self.plot_parameters_container.minimumHeight() + change
                )
            )
        

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
        if isinstance(page, (EISWizardPairplotVector, EISWizardPairplotRaster)):
            fig = page.plot(ax)
        elif isinstance(page, (EISWizardParallelCoordinatesVectorPlot, EISWizardParallelCoordinatesRasterPlot)):
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
