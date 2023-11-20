from qgis.PyQt.QtWidgets import QDialog, QWizard, QTableWidget



from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

# from eis_qgis_plugin.wizard.explore.wizard_explore import EISWizardExplore
# from eis_qgis_plugin.wizard.preprocess.wizard_preprocess import EISWizardPreprocess

FORM_CLASS: QDialog = load_ui("model/model_view.ui")


class EISWizardModeling(QWizard, FORM_CLASS):
    table: QTableWidget

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        # headers = ["Precision", "Recall", "Accuracy", "Support"]
        # self.table.setHorizontalHeaderLabels(headers)
        # self.table.setDisabled(True)
        # self.table.

        # self.layer_tree = QgsLayerTreeView()

        # WORKING?
        # root = QgsProject.instance().layerTreeRoot()
        # model = QgsLayerTreeModel(root)
        # view = QgsLayerTreeView()
        # view.setModel(model)
        # view.show()
