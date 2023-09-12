from qgis.PyQt.QtWidgets import (
    QDialog,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QFrame,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QSizePolicy,
)

from qgis.core import NULL

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from qgis.gui import (
    QgsMapLayerComboBox,
    QgsFieldComboBox,
    QgsColorButton,
    QgsColorRampButton,
    QgsOpacityWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui


FORM_CLASS: QDialog = load_ui("explore/wizard_explore_window_new.ui")


class EISWizardExploreNew(QDialog, FORM_CLASS):
    tab_widget: QTabWidget

    # Tabs
    data_summary_tab: QWidget
    univariate_analysis_tab: QWidget
    bivariate_analysis_tab: QWidget
    multivariate_analysis_tab: QWidget
    geospatial_analysis_tab: QWidget

    # Univariate tab contents
    container: QWidget
    univariate_plot_container: QFrame
    layer_selection: QgsMapLayerComboBox
    field_selection: QgsFieldComboBox
    plot_type_selection: QComboBox
    hue_field_selection: QgsFieldComboBox
    palatte_selection: QgsColorRampButton
    color_selection: QgsColorButton
    opacity_selection: QgsOpacityWidget
    log_scale_selection: QComboBox
    fill_selection: QComboBox
    multiple_selection: QComboBox
    stat_selection: QComboBox
    element_selection: QComboBox
    nr_of_bins_selection: QSpinBox
    bw_adjust_selection: QDoubleSpinBox

    plot_btn: QPushButton

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.plot_btn.clicked.connect(self.plot_distribution)

        self.layer_selection.layerChanged.connect(self.set_layer)
        self.field_selection.fieldChanged.connect(self.set_field)

        self.plot_layout = QVBoxLayout()
        self.univariate_plot_container.setLayout(self.plot_layout)

    def set_layer(self, layer):
        self.field_selection.setLayer(layer)
        self.set_field(self.field_selection.currentField())

    def set_field(self, field_name):
        self.field_selection.setField(field_name)

    def plot_distribution(self):
        for i in reversed(range(self.plot_layout.count())):
            widget = self.plot_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create Seaborn plot
        values = [
            feature.attribute(self.field_selection.currentField())
            for feature in self.layer_selection.currentLayer().getFeatures()
        ]
        values_no_null = [value for value in values if value != NULL]

        fig, ax = plt.subplots()
        sns.histplot(data=values_no_null, ax=ax)
        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar = NavigationToolbar(canvas, self.univariate_plot_container)

        self.plot_layout.addWidget(toolbar)
        self.plot_layout.addWidget(canvas)
