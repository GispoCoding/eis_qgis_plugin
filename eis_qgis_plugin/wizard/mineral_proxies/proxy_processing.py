from typing import Optional

from qgis import processing
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
from eis_qgis_plugin.utils import TEMPORARY_OUTPUT, set_file_widget_placeholder_text

FORM_CLASS_1 = load_ui("mineral_proxies/proxy_workflow1_dist_to_features.ui")
FORM_CLASS_2 = load_ui("mineral_proxies/proxy_workflow2_interpolation.ui")
FORM_CLASS_3 = load_ui("mineral_proxies/proxy_workflow3_define_anomaly.ui")
FORM_CLASS_4 = load_ui("mineral_proxies/proxy_workflow4_interpolation_anomaly.ui")


class EISWizardProxyDistanceToFeatures(QWidget, FORM_CLASS_1):

    ALG_NAME = "eis:distance_computation"

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

        set_file_widget_placeholder_text(self.output_raster_path)

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
        # TODO: Handle case where base raster is not used. Needs modifications to ALG/CLI
        output_raster = self.output_raster_path.filePath()
        processing.runAndLoadResults(
            self.ALG_NAME,
            {
                "input_raster": self.base_raster.currentLayer(),
                "geometries": self.vector_layer.currentLayer(),  # SELECTION NOT INCLUDED!
                "output_raster": output_raster if output_raster != "" else TEMPORARY_OUTPUT
            }
        )

class EISWizardProxyInterpolation(QWidget, FORM_CLASS_2):

    IDW_ALG_NAME = "eis:idw_interpolation"
    KRIGING_ALG_NAME = "eis:kriging_interpolation"

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

        set_file_widget_placeholder_text(self.output_raster_path)

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


    def get_extent(self):
        current_extent = self.extent.outputExtent()
        return "{},{},{},{}".format(
            current_extent.xMinimum(),
            current_extent.xMaximum(),
            current_extent.yMinimum(),
            current_extent.yMaximum()
        )


    def run(self):
        output_raster = self.output_raster_path.filePath()
        interpolation_alg, interpolation_params = self.get_interpolation_alg_and_parameters()
        processing.runAndLoadResults(
            interpolation_alg,
            {
                "input_vector": self.vector_layer.currentLayer(),
                "target_column": self.attribute.currentField(),
                **interpolation_params,
                # TODO: Add base raster, ALG/CLI needs adjustments
                "resolution": self.pixel_size.value(),
                "extent": self.get_extent(),
                "output_raster": output_raster if output_raster != "" else 'TEMPORARY_OUTPUT'
            }
        )


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

        set_file_widget_placeholder_text(self.output_raster_path)

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
        print("Not implemented yet!")


class EISWizardProxyInterpolateAndDefineAnomaly(QWidget, FORM_CLASS_4):

    IDW_ALG_NAME = "eis:idw_interpolation"
    KRIGING_ALG_NAME = "eis:kriging_interpolation"

    def __init__(self, proxy_manager: QWidget, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        
        self.proxy_manager = proxy_manager

        # DELCARE TYPES
        self.workflow_pages: QStackedWidget

        # INTERPOLATION PAGE
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
        self.next_btn: QPushButton

        # ANOMALY PAGE
        self.raster_layer: QgsMapLayerComboBox
        self.band: QgsRasterBandComboBox

        self.anomaly_threshold: QgsDoubleSpinBox
        self.threshold_criteria: QComboBox

        self.anomaly_output_raster_path: QgsFileWidget
        self.anomaly_output_raster_settings: QComboBox
        self.anomaly_output_raster_settings_pages: QStackedWidget
        self.anomaly_base_raster: QgsMapLayerComboBox
        self.anomaly_pixel_size: QgsDoubleSpinBox
        self.anomaly_nodata: QgsDoubleSpinBox
        self.anomaly_extent: QgsExtentGroupBox

        self.anomaly_back_btn: QPushButton
        self.anomaly_run_btn: QPushButton
        self.finish_btn: QPushButton

        self.initialize_interpolation_page()
        self.initialize_anomaly_page()


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


    def initialize_interpolation_page(self):
        # Set filters
        self.vector_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.base_raster.setFilters(QgsMapLayerProxyModel.RasterLayer)

        set_file_widget_placeholder_text(self.output_raster_path)

        # Connect signals
        self.vector_layer.layerChanged.connect(self.attribute.setLayer)
        self.interpolation_method.currentIndexChanged.connect(self.on_interpolation_method_changed)
        self.output_raster_settings.currentIndexChanged.connect(self.on_output_raster_settings_changed)
        self.back_btn.clicked.connect(self.back_interpolate)
        self.run_btn.clicked.connect(self.run_interpolate)
        self.next_btn.clicked.connect(self.next)

        # Initialize layer selection
        self.attribute.setLayer(self.vector_layer.currentLayer())


    def initialize_anomaly_page(self):
        # Set filters
        self.raster_layer.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.anomaly_base_raster.setFilters(QgsMapLayerProxyModel.RasterLayer)

        set_file_widget_placeholder_text(self.anomaly_output_raster_path)

        # Connect signals
        self.raster_layer.layerChanged.connect(self.band.setLayer)
        self.anomaly_output_raster_settings.currentIndexChanged.connect(
            self.on_define_anomaly_output_raster_settings_changed
        )
        self.anomaly_back_btn.clicked.connect(self.back_define_anomaly)
        self.anomaly_run_btn.clicked.connect(self.run_define_anomaly)
        self.finish_btn.clicked.connect(self.finish)

        # Initialize layer selection
        self.band.setLayer(self.raster_layer.currentLayer())


    def on_output_raster_settings_changed(self, i):
        self.output_raster_settings_pages.setCurrentIndex(i)


    def on_define_anomaly_output_raster_settings_changed(self, i):
        self.anomaly_output_raster_settings_pages.setCurrentIndex(i)


    def on_interpolation_method_changed(self, i):
        self.interpolation_method_pages.setCurrentIndex(i)
    

    def back_interpolate(self):
        self.proxy_manager.return_from_proxy_processing()


    def back_define_anomaly(self):
        self.workflow_pages.setCurrentIndex(0)


    def next(self):
        self.workflow_pages.setCurrentIndex(1)

    
    def get_extent(self):
        current_extent = self.extent.outputExtent()
        return "{},{},{},{}".format(
            current_extent.xMinimum(),
            current_extent.xMaximum(),
            current_extent.yMinimum(),
            current_extent.yMaximum()
        )


    def run_interpolate(self):
        output_raster = self.output_raster_path.filePath()
        interpolation_alg, interpolation_params = self.get_interpolation_alg_and_parameters()
        processing.runAndLoadResults(
            interpolation_alg,
            {
                "input_vector": self.vector_layer.currentLayer(),
                "target_column": self.attribute.currentField(),
                **interpolation_params,
                # TODO: Add base raster, ALG/CLI needs adjustments
                "resolution": self.pixel_size.value(),
                "extent": self.get_extent(),
                "output_raster": output_raster if output_raster != "" else 'TEMPORARY_OUTPUT'
            }
        )


    def run_define_anomaly(self):
        print("Not implemented yet!")


    def finish(self):
        self.proxy_manager.return_from_proxy_processing()
