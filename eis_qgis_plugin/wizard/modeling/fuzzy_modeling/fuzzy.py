from typing import List, Tuple

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from qgis.core import QgsMapLayerProxyModel
from qgis.gui import QgsDoubleSpinBox, QgsFileWidget, QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGroupBox,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.fuzzy_modeling.fuzzy_memberships import (
    FuzzyMembership,
    GaussianMembership,
    LargeMembership,
    LinearMembership,
    NearMembership,
    PowerMembership,
    SmallMembership,
)
from eis_qgis_plugin.wizard.modeling.model_data_table import ModelTrainingDataTable

# from eis_qgis_plugin.processing.algorithms.prediction.fuzzy_overlay import (
    
# )

FORM_CLASS: QWidget = load_ui("modeling/wizard_fuzzy_overlay.ui")


class EISWizardFuzzyOverlay(QWidget, FORM_CLASS):
    """
    Class for fuzzy overlay models.
    """

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # DECLARE TYPES

        # Fuzzy membership tab
        self.input_raster_membership: QgsMapLayerComboBox
        self.output_raster_membership: QgsFileWidget
        self.membership_type: QComboBox
        self.membership_parameters_groupbox: QGroupBox
        self.membership_parameters_pages: QStackedWidget

        self.gaussian_function_midpoint: QgsDoubleSpinBox
        self.gaussian_function_spread: QgsDoubleSpinBox

        self.large_function_midpoint: QgsDoubleSpinBox
        self.large_function_spread: QgsDoubleSpinBox

        self.linear_low_bound: QgsDoubleSpinBox
        self.linear_high_bound: QgsDoubleSpinBox

        self.near_function_midpoint: QgsDoubleSpinBox
        self.near_function_spread: QgsDoubleSpinBox

        self.power_low_bound: QgsDoubleSpinBox
        self.power_high_bound: QgsDoubleSpinBox
        self.power_function_exponent: QgsDoubleSpinBox

        self.small_function_midpoint: QgsDoubleSpinBox
        self.small_function_spread: QgsDoubleSpinBox

        self.reset_btn: QPushButton
        self.preview_btn: QPushButton
        self.run_membership_btn: QPushButton

        self.membership_plot_container: QFrame

        # Fuzzy ovelay tab
        self.fuzzy_rasters_box: QGroupBox
        self.fuzzy_rasters_layout: QVBoxLayout
        self.fuzzy_method_box: QGroupBox

        self.and_method: QCheckBox
        self.or_method: QCheckBox
        self.sum_method: QCheckBox
        self.product_method: QCheckBox
        self.gamma_method: QCheckBox
        self.gamma_value: QgsDoubleSpinBox

        self.output_raster_box: QGroupBox
        self.output_raster: QgsFileWidget

        self.run_overlay_btn = QPushButton()

        self.active_overlay_method = self._on_overlay_method_changed()

        # INITIALIZE MEMBERSHIPS AND LINK WIDGETS
        self.initialize_memberships()

        # INITIALIZE UI
        self.initialize_ui()

        # CONNECT SIGNALS
        self.connect_signals()


    def initialize_memberships(self):
        self.memberships = {
            "gaussian": GaussianMembership(
                c = self.gaussian_function_midpoint,
                sigma = self.gaussian_function_spread,
            ),
            "large": LargeMembership(
                c = self.large_function_midpoint,
                k = self.large_function_spread
            ),
            "linear": LinearMembership(
                a = self.linear_low_bound,
                b = self.linear_high_bound
            ),
            "near": NearMembership(
                c = self.near_function_midpoint,
                k = self.near_function_spread
            ),
            "power": PowerMembership(
                a = self.power_low_bound,
                b = self.power_high_bound,
                alpha = self.power_function_exponent
            ),
            
            "small": SmallMembership(
                c = self.small_function_midpoint,
                k = self.small_function_spread
            )
        }


    def initialize_ui(self):
        self.plot_layout = QVBoxLayout()
        self.membership_plot_container.setLayout(self.plot_layout)

        self.input_raster_membership.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.output_raster_membership.setFilter("GeoTiff files (*.tif *.tiff)")

        self.input_rasters_table = ModelTrainingDataTable(self, add_tag_column=False, inital_rows=2)
        self.fuzzy_rasters_layout.addWidget(self.input_rasters_table)


    def connect_signals(self):
        self.reset_btn.clicked.connect(self._on_reset_clicked)
        self.preview_btn.clicked.connect(self._on_preview_clicked)
        self.run_membership_btn.clicked.connect(self._on_run_membership_clicked)
        self.run_overlay_btn.clicked.connect(self._on_run_overlay_clicked)

        self.membership_type.currentIndexChanged['int'].connect(self.membership_parameters_pages.setCurrentIndex)
        self.and_method.stateChanged.connect(self._on_overlay_method_changed)
        self.or_method.stateChanged.connect(self._on_overlay_method_changed)
        self.sum_method.stateChanged.connect(self._on_overlay_method_changed)
        self.product_method.stateChanged.connect(self._on_overlay_method_changed)
        self.gamma_method.stateChanged.connect(self._on_overlay_method_changed)


    def _on_overlay_method_changed(self, _ = None):
        if self.and_method.isChecked():
            self.active_overlay_method = "and"
        elif self.or_method.isChecked():
            self.active_overlay_method = "or"
        elif self.sum_method.isChecked():
            self.active_overlay_method = "sum"
        elif self.product_method.isChecked():
            self.active_overlay_method = "product"
        elif self.gamma_method.isChecked():
            self.active_overlay_method = "gamma"


    def get_active_membership(self) -> Tuple[str, FuzzyMembership]:
        membership_type = self.membership_type.currentText().lower()
        return membership_type, self.memberships[membership_type]
    

    def get_membership_param_values(self, membership_type: str) -> List[float]:
        return [widget.value() for widget in self.membership_params[membership_type].keys()]


    def _on_reset_clicked(self):
        """Reset parameters to defaults."""
        _, membership = self.get_active_membership()
        membership.reset_defaults()


    def _on_preview_clicked(self):
        """Generate a graph of the selected membership function with current parameter values."""
        self.plot()


    def _on_run_membership_clicked(self):
        """Run the selected membership transformation function with current parameter values."""
        _, membership = self.get_active_membership()
        params = membership.get_param_values()
        membership.compute(
            *params,
            self.input_raster_membership.currentLayer(), 
            self.output_raster_membership.filePath()
        )


    def _on_run_overlay_clicked(self):
        """Run fuzzy overlay with the chosen method."""
        if self.and_method.isChecked():
            self.active_overlay_method = "and"
        elif self.or_method.isChecked():
            self.active_overlay_method = "or"
        elif self.sum_method.isChecked():
            self.active_overlay_method = "sum"
        elif self.product_method.isChecked():
            self.active_overlay_method = "product"
        elif self.gamma_method.isChecked():
            self.active_overlay_method = "gamma"
        # TODO

    def plot(self):
        self.close_and_remove_plot()
        fig, ax = plt.subplots()

        membership_type, membership = self.get_active_membership()
        params = membership.get_param_values()
        x_values = membership.x_range(*params)
        sns.lineplot(
            x=x_values,
            y=membership.membership_function(x_values, *params),
            color="green",
            ax=ax,
        )
        plt.xlabel('x')
        plt.ylabel('Membership value')
        plt.title(f'{membership_type.capitalize()} Membership Function')

        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar = NavigationToolbar(canvas, self.membership_plot_container)

        self.plot_layout.addWidget(toolbar)
        self.plot_layout.addWidget(canvas)


    def close_and_remove_plot(self):
        plt.close('all')
        for i in reversed(range(self.plot_layout.count())):
            widget = self.plot_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
