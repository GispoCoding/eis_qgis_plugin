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

FORM_CLASS = load_ui("mineral_proxies/proxy_workflow_binarize.ui")



class EISWizardProxyBinarize(EISWizardProxyProcess, FORM_CLASS):

    ALG_NAME = "eis:binarize"
    WORKFLOW_NAME = "Binarize"

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
        self.binarizing_threshold_label: QLabel
        self.binarizing_threshold: QgsDoubleSpinBox

        self.output_raster_path: QgsFileWidget
        self.output_raster_settings: QComboBox
        self.output_raster_settings_pages: QStackedWidget

        self.initialize()


    def initialize(self):
        self.raster_layer.setFilters(QgsMapLayerProxyModel.RasterLayer)
        super().initialize(self.process_type)


    def on_output_raster_settings_changed(self, i):
        max_height = 50 if i == 0 else 230
        self.output_raster_settings_pages.setMaximumHeight(max_height)
        self.output_raster_settings_pages.setCurrentIndex(i)


    def on_define_anomaly_output_raster_settings_changed(self, i):
        self.output_raster_settings_pages.setCurrentIndex(i)


    def run(self):
        params = {
            "input_raster": self.raster_layer.currentLayer(),
            "threshold": self.binarizing_threshold.value(),
            "output_raster": get_output_path(self.output_raster_path)
        }
        self.executor.configure(self.ALG_NAME, self.feedback)
        self.executor.run(params)