import processing
from qgis.PyQt.QtWidgets import QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QWidget = load_ui("modeling/data_preparation.ui")


class EISMLModelDataPreparation(QWidget, FORM_CLASS):
    
    def __init__(self, parent, model_main) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.model_main = model_main

        self.open_unify_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:unify_rasters'))
        self.open_binarize_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:binarize'))
        self.open_min_max_scale_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:min_max_scaling'))
        self.open_z_score_normalize_btn.clicked.connect(
            lambda _: processing.execAlgorithmDialog('eis:z_score_normalization')
        )
        self.open_winsorize_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:winsorize_transform'))
        self.open_sigmoid_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:sigmoid_transform'))
        self.open_logarithmic_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:log_transform'))
        # self.open_one_hot_encode_btn.clicked.connect(
            # lambda _: processing.execAlgorithmDialog('eis:one_hot_encode')
        # ) #TODO
        self.open_alr_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:alr_transform'))
        self.open_inverse_alr_btn.clicked.connect(
            lambda _: processing.execAlgorithmDialog('eis:inverse_alr_transform')
        )
        self.open_clr_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:clr_transform'))
        self.open_inverse_clr_btn.clicked.connect(
            lambda _: processing.execAlgorithmDialog('eis:inverse_clr_transform')
        )
        self.open_pairwise_logratio_btn.clicked.connect(
            lambda _: processing.execAlgorithmDialog('eis:pairwise_logratio')
        )
        self.open_single_plr_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:single_plr_transform'))
        self.open_single_ilr_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:single_ilr_transform'))
        # self.balance_data_btn.clicked.connect(lambda _: processing.execAlgorithmDialog('eis:balance_data'))
