from typing import Literal, Optional

from qgis.core import QgsMapLayerProxyModel
from qgis.gui import (
    QgsDoubleSpinBox,
    QgsFileWidget,
    QgsMapLayerComboBox,
)
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QGroupBox,
    QLabel,
    QStackedWidget,
    QWidget,
)

from eis_qgis_plugin.eis_wizard.mineral_proxies.proxy_processing import EISWizardProxyProcess
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.misc_utils import get_output_path

FORM_CLASS = load_ui("mineral_proxies/proxy_workflow_proximity_to_anomaly.ui")



class EISWizardProxyProximityToAnomaly(EISWizardProxyProcess, FORM_CLASS):

    ALG_NAME = "eis:proximity_to_anomaly"
    WORKFLOW_NAME = "Proximity to anomaly"

    def __init__(self,
        proxy_manager: QWidget,
        mineral_system: str,
        category: str,
        proxy_name: str,
        mineral_system_component: str,
        process_type: Literal["single_step", "multi_step", "multi_step_final"] = "single_step",
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        self.setupUi(self)
        
        self.mineral_system = mineral_system
        self.mineral_system_component = mineral_system_component
        self.process_type = process_type
        self.category = category
        self.proxy_name = proxy_name
        self.proxy_manager = proxy_manager

        # DECLARE TYPES
        self.raster_layer: QgsMapLayerComboBox
        # self.band: QgsRasterBandComboBox

        self.method_box: QGroupBox
        self.threshold_criteria: QComboBox
        self.threshold_1: QgsDoubleSpinBox
        self.threshold_label_1: QLabel
        self.threshold_2: QgsDoubleSpinBox
        self.threshold_label_2: QLabel
        self.max_distance: QgsDoubleSpinBox
        self.max_distance_value: QgsDoubleSpinBox
        self.anomaly_value: QgsDoubleSpinBox

        self.output_raster_path: QgsFileWidget
        self.output_raster_settings: QComboBox
        self.output_raster_settings_pages: QStackedWidget

        self.initialize()


    def initialize(self):
        self.raster_layer.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.threshold_criteria.currentTextChanged.connect(self.on_threshold_criteria_changed)
        self.on_threshold_criteria_changed("higher")

        super().initialize(self.process_type)


    def on_output_raster_settings_changed(self, i):
        max_height = 50 if i == 0 else 230
        self.output_raster_settings_pages.setMaximumHeight(max_height)
        self.output_raster_settings_pages.setCurrentIndex(i)


    def on_define_anomaly_output_raster_settings_changed(self, i):
        self.output_raster_settings_pages.setCurrentIndex(i)


    def on_threshold_criteria_changed(self, text: str):
        text = text.lower()
        if text == "higher" or text == "lower":
            self.threshold_label_1.setText("Threshold value")
            self.threshold_label_2.hide()
            self.threshold_2.hide()
        else:
            self.threshold_label_1.setText("Threshold value lower")           
            self.threshold_label_2.show()
            self.threshold_2.show()


    def run(self):
        threshold_criteria = self.threshold_criteria.currentIndex()
        anomaly_threshold_2 = self.threshold_2.value()
        if threshold_criteria == 0 or threshold_criteria == 1:
            anomaly_threshold_2 = None

        params = {
            "input_raster": self.raster_layer.currentLayer(),
            "threshold_criteria": self.threshold_criteria.currentIndex(),
            "first_threshold_criteria_value": self.threshold_1.value(),
            "second_threshold_criteria_value": anomaly_threshold_2,
            "max_distance": self.max_distance.value(),
            "max_distance_value": self.max_distance_value.value(),
            "anomaly_value": self.anomaly_value.value(),
            "output_raster": get_output_path(self.output_raster_path)
        }
        self.executor.configure(self.ALG_NAME, self.feedback)
        self.executor.run(params)
