from typing import Optional

from qgis.core import QgsMapLayerProxyModel
from qgis.gui import (
    QgsDoubleSpinBox,
    QgsExtentGroupBox,
    QgsFieldComboBox,
    QgsFieldExpressionWidget,
    QgsMapLayerComboBox,
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


class EISWizardProxyDistanceToFeatures(QWidget, FORM_CLASS_1):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # DELCARE TYPES
        self.vector_layer: QgsMapLayerComboBox
        self.selection: QgsFieldExpressionWidget

        self.output_raster_settings: QComboBox
        self.output_raster_settings_pages: QStackedWidget
        self.base_raster: QgsMapLayerComboBox
        self.pixel_size: QgsDoubleSpinBox
        self.nodata: QgsDoubleSpinBox
        self.extent: QgsExtentGroupBox

        self.run_btn: QPushButton

        # Set filters
        self.vector_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.base_raster.setFilters(QgsMapLayerProxyModel.RasterLayer)

        # Connect signals
        self.vector_layer.layerChanged.connect(self.selection.setLayer)
        self.output_raster_settings.currentIndexChanged.connect(self.output_raster_settings_pages.setCurrentIndex)
        self.run_btn.clicked.connect(self.run)

        # Initialize layer selection
        self.selection.setLayer(self.vector_layer.currentLayer())


    def run(self):
        print("Run clicked")



class EISWizardProxyInterpolation(QWidget, FORM_CLASS_2):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # DELCARE TYPES
        self.vector_layer: QgsMapLayerComboBox
        self.attribute: QgsFieldComboBox

        self.interpolation_method: QComboBox
        self.interpolation_method_pages: QComboBox
        self.power: QgsDoubleSpinBox
        self.kriging_method: QComboBox
        self.variogram_model: QComboBox
        self.coordinates_type: QComboBox

        self.output_raster_settings: QComboBox
        self.output_raster_settings_pages: QStackedWidget
        self.base_raster: QgsMapLayerComboBox
        self.pixel_size: QgsDoubleSpinBox
        self.nodata: QgsDoubleSpinBox
        self.extent: QgsExtentGroupBox

        self.run_btn: QPushButton

        # Set filters
        self.vector_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.base_raster.setFilters(QgsMapLayerProxyModel.RasterLayer)

        # Connect signals
        self.vector_layer.layerChanged.connect(self.attribute.setLayer)
        self.interpolation_method.currentIndexChanged.connect(self.interpolation_method_pages.setCurrentIndex)
        self.output_raster_settings.currentIndexChanged.connect(self.output_raster_settings_pages.setCurrentIndex)
        self.run_btn.clicked.connect(self.run)

        # Initialize layer selection
        self.attribute.setLayer(self.vector_layer.currentLayer())


    def run(self):
        print("Run clicked")
