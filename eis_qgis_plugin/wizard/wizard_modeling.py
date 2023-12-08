from qgis.PyQt.QtWidgets import QComboBox, QDialog, QSizePolicy, QStackedWidget, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.gradient_boosting_classifier import EISWizardGradientBoostingClassifier
from eis_qgis_plugin.wizard.modeling.gradient_boosting_regressor import EISWizardGradientBoostingRegressor
from eis_qgis_plugin.wizard.modeling.logistic_regression import EISWizardLogisticRegression
from eis_qgis_plugin.wizard.modeling.random_forests_classifier import EISWizardRandomForestsClassifier
from eis_qgis_plugin.wizard.modeling.random_forests_regressor import EISWizardRandomForestsRegressor

# from eis_qgis_plugin.wizard.explore.wizard_explore import EISWizardExplore
# from eis_qgis_plugin.wizard.preprocess.wizard_preprocess import EISWizardPreprocess

FORM_CLASS: QDialog = load_ui("model/wizard_model_new.ui")


class EISWizardModeling(QWidget, FORM_CLASS):
    # table: QTableWidget
    model_selection: QComboBox
    model_parameters_container: QStackedWidget

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.model_selection.currentIndexChanged['int'].connect(self.model_parameters_container.setCurrentIndex)

        self.model_parameters_container.currentChanged.connect(self.resize_parameter_container)

        self.pages = [
            EISWizardGradientBoostingClassifier(self),
            EISWizardGradientBoostingRegressor(self),
            EISWizardRandomForestsClassifier(self),
            EISWizardRandomForestsRegressor(self),
            EISWizardLogisticRegression(self),
        ]

        for i, page in enumerate(self.pages):
            self.model_parameters_container.insertWidget(i, page)


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

        # Create pages for parameters

    def resize_parameter_container(self, index):
        """Resize the QStackedWidget that contains model parameters according to the needed size."""
        widget = self.model_parameters_container.widget(index)
        if widget:
            self.model_parameters_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.model_parameters_container.setMinimumHeight(widget.height())
