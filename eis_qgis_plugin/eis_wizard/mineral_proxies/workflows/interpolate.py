from typing import Literal, Optional

from qgis.core import QgsMapLayerProxyModel
from qgis.gui import (
    QgsDoubleSpinBox,
    QgsFieldComboBox,
    QgsFileWidget,
    QgsMapLayerComboBox,
)
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QStackedWidget,
    QWidget,
)

from eis_qgis_plugin.eis_wizard.mineral_proxies.proxy_processing import EISWizardProxyProcess
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.misc_utils import get_output_path

FORM_CLASS = load_ui("mineral_proxies/proxy_workflow2_interpolation.ui")


class EISWizardProxyInterpolate(EISWizardProxyProcess, FORM_CLASS):

    IDW_ALG_NAME = "eis:idw_interpolation"
    KRIGING_ALG_NAME = "eis:kriging_interpolation"
    WORKFLOW_NAME = "Interpolation"

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

        # DELCARE TYPES
        self.vector_layer: QgsMapLayerComboBox
        self.attribute: QgsFieldComboBox

        self.interpolation_method: QComboBox
        self.interpolation_method_pages: QComboBox
        self.power: QgsDoubleSpinBox
        self.kriging_method: QComboBox
        self.variogram_model: QComboBox
        self.coordinates_type: QComboBox

        self.output_raster_path: QgsFileWidget
        self.output_raster_settings: QComboBox
        self.output_raster_settings_pages: QStackedWidget

        self.initialize()


    def initialize(self):
        self.vector_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.vector_layer.layerChanged.connect(self.attribute.setLayer)
        self.interpolation_method.currentIndexChanged.connect(self.on_interpolation_method_changed)
        self.attribute.setLayer(self.vector_layer.currentLayer())

        super().initialize(self.process_type)

    
    def get_interpolation_alg_and_parameters(self):
        if self.interpolation_method.currentIndex() == 0:  # IDW
            params = {
                "power": self.power.value()
            }
            return self.IDW_ALG_NAME, params
        else:  # Kriging
            params = {
                "method": self.kriging_method.currentIndex(),
                "variogram_model": self.variogram_model.currentIndex(),
                "coordinates_type": self.coordinates_type.currentIndex()
            }
            return self.KRIGING_ALG_NAME, params


    def on_output_raster_settings_changed(self, i):
        max_height = 50 if i == 0 else 230
        self.output_raster_settings_pages.setMaximumHeight(max_height)
        self.output_raster_settings_pages.setCurrentIndex(i)


    def on_interpolation_method_changed(self, i):
        self.interpolation_method_pages.setCurrentIndex(i)


    def run(self):
        interpolation_alg, interpolation_params = self.get_interpolation_alg_and_parameters()
        output_raster_params = self.get_output_raster_params()
        if output_raster_params is None or self.executor.is_running:
            return

        params = {
            "input_vector": self.vector_layer.currentLayer(),
            "target_column": self.attribute.currentField(),
            **interpolation_params,
            **output_raster_params,
            "output_raster": get_output_path(self.output_raster_path)
        }
        self.executor.configure(interpolation_alg, self.feedback)
        self.executor.run(params)
