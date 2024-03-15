from typing import Optional

from qgis.core import QgsMapLayerProxyModel
from qgis.gui import (
    QgsDoubleSpinBox,
    QgsExtentGroupBox,
    QgsFieldComboBox,
    QgsFieldExpressionWidget,
    QgsFileWidget,
    QgsMapLayerComboBox,
    QgsRasterBandComboBox,
)
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QPushButton,
    QStackedWidget,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS_1 = load_ui("mineral_proxies/proxy_workflow1_dist_to_features.ui")
FORM_CLASS_2 = load_ui("mineral_proxies/proxy_workflow2_interpolation.ui")
FORM_CLASS_3 = load_ui("mineral_proxies/proxy_workflow3_define_anomaly.ui")


class EISWizardProxyDistanceToFeatures(QWidget, FORM_CLASS_1):

    def __init__(self, proxy_manager: QWidget, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.proxy_manager = proxy_manager

        # DELCARE TYPES
        self.vector_layer: QgsMapLayerComboBox
        self.selection: QgsFieldExpressionWidget
    
        self.output_raster_path: QgsFileWidget
        self.output_raster_settings: QComboBox
        self.output_raster_settings_pages: QStackedWidget
        self.base_raster: QgsMapLayerComboBox
        self.pixel_size: QgsDoubleSpinBox
        self.nodata: QgsDoubleSpinBox
        self.extent: QgsExtentGroupBox

        self.back_btn: QPushButton
        self.run_btn: QPushButton

        # Set filters
        self.vector_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.base_raster.setFilters(QgsMapLayerProxyModel.RasterLayer)

        # Connect signals
        self.vector_layer.layerChanged.connect(self.selection.setLayer)
        self.output_raster_settings.currentIndexChanged.connect(self.on_output_raster_settings_changed)
        self.back_btn.clicked.connect(self.back)
        self.run_btn.clicked.connect(self.run)

        # Initialize layer selection
        self.selection.setLayer(self.vector_layer.currentLayer())
    

    def on_output_raster_settings_changed(self, i):
        max_height = 50 if i == 0 else 230
        self.output_raster_settings_pages.setMaximumHeight(max_height)
        self.output_raster_settings_pages.setCurrentIndex(i)

    
    def back(self):
        self.proxy_manager.return_from_proxy_processing()


    def run(self):
        print("Run clicked")



class EISWizardProxyInterpolation(QWidget, FORM_CLASS_2):

    def __init__(self, proxy_manager: QWidget, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

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
        self.base_raster: QgsMapLayerComboBox
        self.pixel_size: QgsDoubleSpinBox
        self.nodata: QgsDoubleSpinBox
        self.extent: QgsExtentGroupBox

        self.back_btn: QPushButton
        self.run_btn: QPushButton

        # Set filters
        self.vector_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.base_raster.setFilters(QgsMapLayerProxyModel.RasterLayer)

        # Connect signals
        self.vector_layer.layerChanged.connect(self.attribute.setLayer)
        self.interpolation_method.currentIndexChanged.connect(self.on_interpolation_method_changed)
        self.output_raster_settings.currentIndexChanged.connect(self.on_output_raster_settings_changed)
        self.back_btn.clicked.connect(self.back)
        self.run_btn.clicked.connect(self.run)

        # Initialize layer selection
        self.attribute.setLayer(self.vector_layer.currentLayer())


    def on_output_raster_settings_changed(self, i):
        max_height = 50 if i == 0 else 230
        self.output_raster_settings_pages.setMaximumHeight(max_height)
        self.output_raster_settings_pages.setCurrentIndex(i)

    
    def on_interpolation_method_changed(self, i):
        max_height = 50 if i == 0 else 110
        self.interpolation_method_pages.setMaximumHeight(max_height)
        self.interpolation_method_pages.setCurrentIndex(i)


    def back(self):
        self.proxy_manager.return_from_proxy_processing()


    def run(self):
        print("Run clicked")



class EISWizardProxyDefineAnomaly(QWidget, FORM_CLASS_3):

    def __init__(self, proxy_manager: QWidget, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        
        self.proxy_manager = proxy_manager

        # DELCARE TYPES
        self.raster_layer: QgsMapLayerComboBox
        self.band: QgsRasterBandComboBox

        self.anomaly_threshold: QgsDoubleSpinBox
        self.threshold_criteria: QComboBox

        self.output_raster_path: QgsFileWidget
        self.output_raster_settings: QComboBox
        self.output_raster_settings_pages: QStackedWidget
        self.base_raster: QgsMapLayerComboBox
        self.pixel_size: QgsDoubleSpinBox
        self.nodata: QgsDoubleSpinBox
        self.extent: QgsExtentGroupBox

        self.back_btn: QPushButton
        self.run_btn: QPushButton

        # Set filters
        self.raster_layer.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.base_raster.setFilters(QgsMapLayerProxyModel.RasterLayer)

        # Connect signals
        self.raster_layer.layerChanged.connect(self.band.setLayer)
        self.output_raster_settings.currentIndexChanged.connect(self.on_output_raster_settings_changed)
        self.back_btn.clicked.connect(self.back)
        self.run_btn.clicked.connect(self.run)

        # Initialize layer selection
        self.band.setLayer(self.raster_layer.currentLayer())


    def on_output_raster_settings_changed(self, i):
        max_height = 230 if i == 2 else 50
        self.output_raster_settings_pages.setMaximumHeight(max_height)
        self.output_raster_settings_pages.setCurrentIndex(i)


    def back(self):
        self.proxy_manager.return_from_proxy_processing()


    def run(self):
        print("Run clicked")
