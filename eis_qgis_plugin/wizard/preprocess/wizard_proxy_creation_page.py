from PyQt5.QtWidgets import QWizardPage

from qgis import processing

from ..explore.wizard_explore_new import EISWizardExploreNew
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QWizardPage = load_ui("preprocess/wizard_proxy_creation.ui")


class EISWizardProxyCreation(QWizardPage, FORM_CLASS):
    def __init__(self) -> None:
        super().__init__()
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
            lambda: processing.execAlgorithmDialog("eis:idw_interpolation", {})
        )
        self.interpolate_kriging_btn.clicked.connect(
            lambda: processing.execAlgorithmDialog("eis:kriging_interpolation", {})
        )
        # self.binarize_btn.clicked.connect(processing.execAlgorithmDialog("eis:", {}) )

    def open_explore(self):
        self.explore_window = EISWizardExploreNew(self)
        self.explore_window.show()
