import processing
from qgis.PyQt.QtWidgets import QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QWidget = load_ui("eda/wizard_exploratory_analysis.ui")


class EISExploratoryAnalysis(QWidget, FORM_CLASS):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.open_chi_square_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:chi_square_test'))
        self.open_dbscan_vector_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:dbscan_vector'))
        self.open_dbscan_raster_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:dbscan_raster'))
        self.open_k_means_vector_btn.clicked.connect(
            lambda _: processing.execAlgorithmDialog('eis:k_means_clustering_vector')
        )
        self.open_k_means_raster_btn.clicked.connect(
            lambda _: processing.execAlgorithmDialog('eis:k_means_clustering_raster')
        )
        self.open_local_morans_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:local_morans_i'))
        self.open_normality_vector_btn.clicked.connect(
            lambda _: processing.execAlgorithmDialog('eis:normality_test_vector')
        )
        self.open_normality_raster_btn.clicked.connect(
            lambda _: processing.execAlgorithmDialog('eis:normality_test_raster')
        )
        self.open_pca_vector_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:compute_pca_vector'))
        self.open_pca_raster_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:compute_pca_raster'))
        
        