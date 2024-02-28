import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from qgis.core import QgsMapLayerProxyModel
from qgis.gui import QgsFieldComboBox, QgsFieldExpressionWidget, QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import QDialog, QSizePolicy, QVBoxLayout, QWizardPage

import eis_qgis_plugin.libs.seaborn as sns

from ...explore.old.wizard_explore import EISWizardExplore


class EISWizardProxy(QWizardPage):
    layer_selection: QgsMapLayerComboBox
    attribute_selection: QgsFieldComboBox
    field_expression: QgsFieldExpressionWidget

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.layer_selection.setFilters(QgsMapLayerProxyModel.VectorLayer)

        self.layer_selection.layerChanged.connect(self.set_layer)
        self.attribute_selection.fieldChanged.connect(self.set_field)

        # self.compute_and_plot_btn.clicked.connect(self.show_plot)
        # self.compute_and_plot_btn.clicked.connect(self.show_plot2)
        self.create_file_btn.clicked.connect(self.create_file)
        self.open_explore_btn.clicked.connect(self.open_explore)

    def set_layer(self, layer):
        self.attribute_selection.setLayer(layer)
        self.set_field(self.attribute_selection.currentField())

    def set_field(self, field_name):
        self.field_expression.setField(field_name)

    def open_explore(self):
        self.explore_window = EISWizardExplore(self)
        self.explore_window.show()

    def create_file(self):
        pass

    def show_plot2(self):
        layout = QVBoxLayout()

        # Create Seaborn plot
        penguins = sns.load_dataset("penguins")
        fig, ax = plt.subplots()
        sns.histplot(data=penguins, x="flipper_length_mm", ax=ax)
        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        toolbar = NavigationToolbar(canvas, self.plot_widget)
        layout.addWidget(toolbar)
        layout.addWidget(canvas)

        self.plot_widget.setLayout(layout)

    def show_plot(self):
        dialog = QDialog()
        dialog.setWindowTitle("Seaborn Plot")
        dialog.resize(500, 400)

        layout = QVBoxLayout()

        # Create Seaborn plot
        tips = sns.load_dataset("tips")
        fig, ax = plt.subplots()
        sns.barplot(x="day", y="total_bill", data=tips, ax=ax)
        # plt.show()

        # Embed plot into PyQt5 dialog
        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar = NavigationToolbar(canvas, dialog)
        layout.addWidget(toolbar)
        layout.addWidget(canvas)

        dialog.setLayout(layout)
        dialog.exec_()
