from qgis.PyQt.QtWidgets import (
    QDialog,
)

from qgis.core import (
    QgsMapLayerProxyModel
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QDialog = load_ui("preprocess/proxy_type1.ui")

class EISWizardProxy(QDialog, FORM_CLASS):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.layer_selection.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.layer_selection.layerChanged.connect(self.set_layer)


    def set_layer(self, layer):
        self.field_combo_box.setLayer(layer)

    
