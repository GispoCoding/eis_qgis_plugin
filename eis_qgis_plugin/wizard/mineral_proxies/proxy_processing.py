from typing import Optional

from qgis.core import QgsMapLayerProxyModel
from qgis.gui import QgsFieldExpressionWidget, QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import QPushButton, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS = load_ui("mineral_proxies/proxy_workflow1_dist_to_features.ui")


class EISWizardProxyDistanceToFeatures(QWidget, FORM_CLASS):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # DELCARE TYPES
        self.vector_layer: QgsMapLayerComboBox
        self.selection: QgsFieldExpressionWidget
        self.base_raster: QgsMapLayerComboBox

        self.run_btn: QPushButton

        # Set filters
        self.vector_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.base_raster.setFilters(QgsMapLayerProxyModel.RasterLayer)

        # Connect signals
        self.vector_layer.layerChanged.connect(self.selection.setLayer)
        self.run_btn.clicked.connect(self.run)


    def run(self):
        print("Run clicked")
