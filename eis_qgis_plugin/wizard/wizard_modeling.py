from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialog,
    QStackedWidget,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.fuzzy_overlay import EISWizardFuzzyOverlay
from eis_qgis_plugin.wizard.modeling.gradient_boosting import EISWizardGradientBoosting
from eis_qgis_plugin.wizard.modeling.logistic_regression import EISWizardLogisticRegression
from eis_qgis_plugin.wizard.modeling.ml_model_template import ModelType
from eis_qgis_plugin.wizard.modeling.random_forest import EISWizardRandomForest

FORM_CLASS: QDialog = load_ui("wizard_modeling.ui")


class EISWizardModeling(QWidget, FORM_CLASS):
    """
    Class for the whole modeling view.
    
    Views for each model type are created separately and added to the stacked widget.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.model_selection: QComboBox
        self.model_pages: QStackedWidget

        self.model_selection.currentIndexChanged['int'].connect(self.model_pages.setCurrentIndex)
        self.initialize_model_pages()
    

    def initialize_model_pages(self):
        """Create pages for each model type in the stacked widget."""
        self.pages = [
            EISWizardLogisticRegression(self),
            EISWizardRandomForest(self, ModelType.CLASSIFIER),
            EISWizardRandomForest(self, ModelType.REGRESSOR),
            EISWizardGradientBoosting(self, ModelType.CLASSIFIER),
            EISWizardGradientBoosting(self, ModelType.REGRESSOR),
            EISWizardFuzzyOverlay(self)
        ]

        for i, page in enumerate(self.pages):
            self.model_pages.insertWidget(i, page)
