from PyQt5.QtWidgets import QWizardPage
from qgis import processing
from qgis.PyQt.QtWidgets import (
    QDialog,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

from ...explore.old.wizard_explore import EISWizardExplore

FORM_CLASS: QDialog = load_ui("preprocess/proxy_view_with_links.ui")


class EISWizardProxyCreation(QWizardPage, FORM_CLASS):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.open_explore_btn.clicked.connect(self.open_explore)

        self.extract_by_attribute_btn.clicked.connect(
            lambda: processing.execAlgorithmDialog("qgis:extractbyattribute", {})
        )
        self.extract_by_expression_btn.clicked.connect(
            lambda: processing.execAlgorithmDialog("qgis:extractbyexpression", {})
        )

        self.calculate_distances_vector_btn.clicked.connect(
            lambda: processing.execAlgorithmDialog("eis:distance_computation", {})
        )
        self.calculate_distances_raster_btn.clicked.connect(
            lambda: processing.execAlgorithmDialog("eis:distance_computation", {})
        )
        self.calculate_density_btn.clicked.connect(
            lambda: processing.execAlgorithmDialog("eis:vector_density", {})
        )
        self.interpolate_idw_btn.clicked.connect(
            lambda: processing.execAlgorithmDialog("eis:simple_idw", {})
        )
        self.interpolate_kriging_btn.clicked.connect(
            lambda: processing.execAlgorithmDialog("eis:kriging_interpolation", {})
        )
        # self.binarize_btn.clicked.connect(processing.execAlgorithmDialog("eis:", {}) )

    def open_explore(self):
        self.explore_window = EISWizardExplore(self)
        self.explore_window.show()
