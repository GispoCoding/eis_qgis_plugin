from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialog,
    QStackedWidget,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.fuzzy_modeling.fuzzy import EISWizardFuzzyModeling
from eis_qgis_plugin.wizard.modeling.machine_learning.models.gradient_boosting import EISWizardGradientBoosting
from eis_qgis_plugin.wizard.modeling.machine_learning.models.logistic_regression import EISWizardLogisticRegression
from eis_qgis_plugin.wizard.modeling.machine_learning.models.random_forest import EISWizardRandomForest
from eis_qgis_plugin.wizard.modeling.model_manager import ModelManager
from eis_qgis_plugin.wizard.modeling.model_utils import ModelKind

FORM_CLASS: QDialog = load_ui("wizard_modeling.ui")


class EISWizardModeling(QWidget, FORM_CLASS):
    """
    Class for the whole modeling view.
    
    Views for each model type are created separately and added to the stacked widget.
    """

    def __init__(self, parent=None, model_manager: ModelManager = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.model_selection: QComboBox
        self.model_pages: QStackedWidget

        self.model_manager = model_manager

        self.model_selection.currentIndexChanged['int'].connect(self.model_pages.setCurrentIndex)
        self.initialize_model_pages()
    

    def initialize_model_pages(self):
        """Create pages for each model type in the stacked widget."""
        self.pages = [
            EISWizardLogisticRegression(self),
            EISWizardRandomForest(self, ModelKind.CLASSIFIER),
            EISWizardRandomForest(self, ModelKind.REGRESSOR),
            EISWizardGradientBoosting(self, ModelKind.CLASSIFIER),
            EISWizardGradientBoosting(self, ModelKind.REGRESSOR),
            EISWizardFuzzyModeling(self)
        ]

        for i, page in enumerate(self.pages):
            self.model_pages.insertWidget(i, page)
