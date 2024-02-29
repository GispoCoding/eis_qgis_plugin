from qgis.core import QgsMapLayerProxyModel
from qgis.gui import QgsDoubleSpinBox, QgsFileWidget, QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGroupBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.model_data_table import ModelTrainingDataTable

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

        self.membership_graph_container: QFrame

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

        # INITIALIZE UI
        self.initialize_ui()

        # CONNECT SIGNALS
        self.connect_signals()


    def initialize_ui(self):
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


    def _on_reset_clicked(self):
        """Reset parameters to defaults."""
        membership_type = self.membership_type.currentText().lower()
        if membership_type == "gaussian":
            self.gaussian_function_midpoint.setValue(10)
            self.gaussian_function_spread.setValue(0.01)

        elif membership_type == "large":
            self.large_function_midpoint.setValue(50)
            self.large_function_spread.setValue(5)

        elif membership_type == "linear":
            self.linear_low_bound.setValue(0)
            self.linear_high_bound.setValue(1)

        elif membership_type == "near":
            self.near_function_midpoint.setValue(50)
            self.near_function_spread.setValue(5)

        elif membership_type == "power":
            self.power_low_bound.setValue(0)
            self.power_high_bound.setValue(1)
            self.power_function_exponent.setValue(2)

        elif membership_type == "small":
            self.small_function_midpoint.setValue(50)
            self.small_function_spread.setValue(5)


    def _on_preview_clicked(self):
        """Generate a graph of the selected membership function with current parameter values."""
        pass


    def _on_run_membership_clicked(self):
        """Run the selected membership transformation function with current parameter values."""
        self.input_raster_membership.currentLayer()
        self.output_raster_membership.filePath()
        membership_type = self.membership_type.currentText().lower()

        if membership_type == "gaussian":
            self.gaussian_function_midpoint
            self.gaussian_function_spread
        elif membership_type == "large":
            self.large_function_midpoint
            self.large_function_spread
        elif membership_type == "linear":
            self.linear_low_bound
            self.linear_high_bound
        elif membership_type == "near":
            self.near_function_midpoint
            self.near_function_spread
        elif membership_type == "power":
            self.power_low_bound
            self.power_high_bound
            self.power_function_exponent
        elif membership_type == "small":
            self.small_function_midpoint
            self.small_function_spread


    def _on_run_overlay_clicked(self):
        """Run fuzzy overlay with the chosen method."""
        pass
