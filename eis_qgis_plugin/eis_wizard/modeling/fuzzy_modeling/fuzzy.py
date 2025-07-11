from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from qgis.core import QgsApplication, QgsMapLayerProxyModel, QgsProject, QgsRasterLayer
from qgis.gui import QgsDoubleSpinBox, QgsFileWidget, QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialogButtonBox,
    QFrame,
    QGroupBox,
    QProgressBar,
    QSizePolicy,
    QStackedWidget,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

import eis_qgis_plugin.libs.seaborn as sns
from eis_qgis_plugin.eis_wizard.modeling.fuzzy_modeling.fuzzy_memberships import (
    FuzzyMembership,
    GaussianMembership,
    LargeMembership,
    LinearMembership,
    NearMembership,
    PowerMembership,
    SmallMembership,
)
from eis_qgis_plugin.eis_wizard.modeling.machine_learning.data_preparation import EISMLModelDataPreparation
from eis_qgis_plugin.eis_wizard.modeling.model_data_table import ModelTrainingDataTable
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.algorithm_execution import AlgorithmExecutor
from eis_qgis_plugin.utils.misc_utils import (
    add_output_layer_to_group,
    # apply_color_ramp_to_raster_layer,
    get_output_layer_name,
    get_output_path,
    set_placeholder_text,
)
from eis_qgis_plugin.utils.model_feedback import EISProcessingFeedback
from eis_qgis_plugin.utils.settings_manager import EISSettingsManager

FORM_CLASS: QWidget = load_ui("modeling/wizard_fuzzy_modeling.ui")


class EISWizardFuzzyModeling(QWidget, FORM_CLASS):
    """
    Class for fuzzy overlay models.
    """

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # DECLARE TYPES
        self.fuzzy_modeling_tabs: QTabWidget

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
        
        self.button_box_memberships: QDialogButtonBox

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

        self.output_raster_overlay_box: QGroupBox
        self.output_raster_overlay: QgsFileWidget

        self.button_box_overlay: QDialogButtonBox

        self.overlay_log: QTextEdit
        self.overlay_progress_bar: QProgressBar

        self.data_preparation = EISMLModelDataPreparation(parent=self.fuzzy_modeling_tabs, model_main=self)
        self.fuzzy_modeling_tabs.insertTab(0, self.data_preparation, "Data preparation")
        self.fuzzy_modeling_tabs.setCurrentIndex(0)

        self.overlay_feedback = EISProcessingFeedback(self.overlay_log, self.overlay_progress_bar)
        self.executor = AlgorithmExecutor()

        # INITIALIZE MEMBERSHIPS AND LINK WIDGETS
        self.initialize_memberships()

        # INITIALIZE UI
        self.initialize_ui()

        # CONNECT SIGNALS
        self.connect_signals()


    def on_algorithm_executor_finished(self, result, _):
        if self.overlay_feedback.no_errors:
            for (layer_name, output_layer, output_path) in self.output_layers:
                layer = QgsRasterLayer(result[output_layer], get_output_layer_name(output_path, layer_name))
                if EISSettingsManager.get_layer_group_selection():
                    add_output_layer_to_group(layer, "Modeling — Fuzzy")
                else:
                    QgsProject.instance().addMapLayer(layer, True)

                # apply_color_ramp_to_raster_layer(layer, EISSettingsManager.get_raster_color_ramp())


    def on_algorithm_executor_error(self, error_message: str):
        pass


    def on_algorithm_executor_terminated(self):
        self.overlay_feedback = EISProcessingFeedback(
            text_edit=self.overlay_log, progress_bar=self.overlay_progress_bar
        )


    def initialize_memberships(self):
        """Initializes all possible membership instances in a dictionary and links relevant widgets to them."""
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
        """UI-related initialization."""
        # Memberships
        self.plot_layout = QVBoxLayout()
        self.membership_plot_container.setLayout(self.plot_layout)

        self.input_raster_membership.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.output_raster_membership.setFilter("GeoTiff files (*.tif *.tiff)")
        set_placeholder_text(self.output_raster_membership)

        # Overlay
        self.input_rasters_table = ModelTrainingDataTable(self, add_tag_column=False, inital_rows=2, min_rows=2)
        self.fuzzy_rasters_layout.addWidget(self.input_rasters_table)

        self.output_raster_overlay.setFilter("GeoTiff files (*.tif *.tiff)")
        set_placeholder_text(self.output_raster_overlay)


    def connect_signals(self):
        """Connect signals emitted by widgets to functions."""
        self.memberships_run_btn = self.button_box_memberships.button(QDialogButtonBox.Ok)
        self.memberships_run_btn.setText("Run")
        self.memberships_run_btn.setIcon(QgsApplication.getThemeIcon("mActionStart.svg"))
        self.button_box_memberships.button(QDialogButtonBox.RestoreDefaults).setAutoDefault(False)
        self.preview_btn = self.button_box_memberships.addButton("Preview", QDialogButtonBox.ActionRole)
        self.preview_btn.setIcon(QgsApplication.getThemeIcon("mActionZoomTo.svg"))

        self.cancel_overlay_btn = self.button_box_overlay.button(QDialogButtonBox.Cancel)
        self.cancel_overlay_btn.setText("Cancel")
        self.overlay_run_btn = self.button_box_overlay.button(QDialogButtonBox.Ok)
        self.overlay_run_btn.setText("Run")
        self.overlay_run_btn.setIcon(QgsApplication.getThemeIcon("mActionStart.svg"))

        self.button_box_memberships.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self._on_reset_clicked)
        self.preview_btn.clicked.connect(self._on_preview_clicked)
        self.memberships_run_btn.clicked.connect(self._on_run_membership_clicked)
        self.overlay_run_btn.clicked.connect(self._on_run_overlay_clicked)

        self.membership_type.currentIndexChanged['int'].connect(self.membership_parameters_pages.setCurrentIndex)

        self.executor.finished.connect(self.on_algorithm_executor_finished)
        self.executor.terminated.connect(self.on_algorithm_executor_terminated)
        self.executor.error.connect(self.on_algorithm_executor_error)


    def get_active_membership(self) -> Tuple[str, FuzzyMembership]:
        """Returns active fuzzy membership (name, class instance)."""
        membership_type = self.membership_type.currentText().lower()
        return membership_type, self.memberships[membership_type]


    def _on_reset_clicked(self):
        """Reset active fuzzy membership parameters to defaults."""
        _, membership = self.get_active_membership()
        membership.reset_defaults()


    def _on_preview_clicked(self):
        """Create a plot of the selected membership function with its current parameter values."""
        self.plot()


    def _on_run_membership_clicked(self):
        """Run the selected membership transformation function with current parameter values."""
        _, membership = self.get_active_membership()
        params = membership.get_param_values()
        membership.compute(
            *params,
            self.input_raster_membership.currentLayer(), 
            get_output_path(self.output_raster_membership)
        )


    def _on_run_overlay_clicked(self):
        """Run fuzzy overlay with the chosen method."""
        # The order here needs to match the order of overlay methods in processing algorithm
        if self.and_method.isChecked():
            overlay_method_index = 0  # And
        elif self.or_method.isChecked():
            overlay_method_index = 1  # Or
        elif self.sum_method.isChecked():
            overlay_method_index = 2  # Sum
        elif self.product_method.isChecked():
            overlay_method_index = 3  # Product
        elif self.gamma_method.isChecked():
            overlay_method_index = 4  # Gamma
        else:
            raise ValueError("No overlay method selected, cannot run fuzzy ovelay.")

        params = {
            'input_rasters': self.input_rasters_table.get_layers(),
            'overlay_method': overlay_method_index,
            'gamma': self.gamma_value.value(),
            'output_raster': get_output_path(self.output_raster_overlay)
        }
        self.output_layers = [("Output overlay raster", "output_raster", self.output_raster_overlay)]
        self.executor.configure("eis:fuzzy_overlay", self.overlay_feedback)
        self.executor.run(params)


    @staticmethod
    def get_selected_raster_range(layer: QgsRasterLayer) -> Tuple[float, float]:
        stats = layer.dataProvider().bandStatistics(1)
        return stats.minimumValue, stats.maximumValue


    def plot(self):
        """Create plot for membership function and handle related widget clearing and setting."""
        self.close_and_remove_plot()
        fig, ax = plt.subplots()

        membership_type, membership = self.get_active_membership()
        params = membership.get_param_values()
        min_value, max_value = self.get_selected_raster_range(self.input_raster_membership.currentLayer())
        x_values = membership.x_range_dynamic(min_value, max_value)
        y_values = membership.membership_function(x_values, *params)
        if isinstance(y_values, pd.DataFrame) or isinstance(y_values, pd.Series):
            y_values = y_values.to_numpy()

        sns.lineplot(
            x=x_values,
            y=y_values,
            color="green",
            ax=ax,
        )
        plt.xlabel('Input raster value')
        plt.ylabel('Output membership raster value')
        plt.title(f'{membership_type.capitalize()} membership')

        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar = NavigationToolbar(canvas, self.membership_plot_container)

        self.plot_layout.addWidget(toolbar)
        self.plot_layout.addWidget(canvas)


    def close_and_remove_plot(self):
        """Close and remove existing plots."""
        plt.close('all')
        for i in reversed(range(self.plot_layout.count())):
            widget = self.plot_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
