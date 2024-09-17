from typing import Any, Dict, List

from qgis.PyQt.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from eis_qgis_plugin.wizard.modeling.machine_learning.application import EISMLModelApplication
from eis_qgis_plugin.wizard.modeling.machine_learning.data_preparation import EISMLModelDataPreparation
from eis_qgis_plugin.wizard.modeling.machine_learning.testing import EISMLModelTesting
from eis_qgis_plugin.wizard.modeling.machine_learning.training import EISMLModelTraining
from eis_qgis_plugin.wizard.modeling.machine_learning.training_mlp import EISMLModelTrainingMLP
from eis_qgis_plugin.wizard.modeling.model_manager import ModelManager
from eis_qgis_plugin.wizard.utils.misc_utils import CLASSIFIER_METRICS, REGRESSOR_METRICS, ModelKind


class EISMLModel(QWidget):
    """Parent class for ML model classes in EIS Wizard."""

    ROW_HEIGHT = 26
    
    def __init__(self, parent, model_type: str, model_kind: ModelKind) -> None:
        super().__init__(parent)

        self.modeling_tabs = QTabWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.modeling_tabs)

        self.setLayout(layout)

        self.model_type = model_type
        self.model_kind = model_kind
        self.model_manager: ModelManager = self.parent().model_manager
        self.model_manager.models_updated.connect(self.update_model_selections)

        self.data_preparation = EISMLModelDataPreparation(parent=self.modeling_tabs, model_main=self)
        self.modeling_tabs.addTab(self.data_preparation, "Data preparation")

        if self.model_type[:3] == "MLP":
            self.training = EISMLModelTrainingMLP(parent=self.modeling_tabs, model_main=self)
        else:
            self.training = EISMLModelTraining(parent=self.modeling_tabs, model_main=self)
        self.modeling_tabs.addTab(self.training, "Training")

        self.testing = EISMLModelTesting(parent=self.modeling_tabs, model_main=self)
        self.modeling_tabs.addTab(self.testing, "Testing")

        self.application = EISMLModelApplication(parent=self.modeling_tabs, model_main=self)
        self.modeling_tabs.addTab(self.application, "Application")


    def update_model_selections(self):
        models = []
        for model in self.model_manager.get_all_models():
            if self.model_manager.get_model_info(model).model_type == self.model_type:
                models.append(model)
        self.testing.update_selectable_models(models)
        self.application.update_selectable_models(models)


    def get_model_type(self) -> str:
        return self.model_type
    

    def get_model_kind(self) -> str:
        return "classifier" if self.model_kind == ModelKind.CLASSIFIER else "regressor"


    def get_valid_metrics(self) -> List[str]:
        return CLASSIFIER_METRICS if self.model_kind == ModelKind.CLASSIFIER else REGRESSOR_METRICS


    def get_alg_name(self) -> str:
        return self.alg_name
    

    def get_model_manager(self) -> ModelManager:
        return self.model_manager


    def get_data_preparation_tab(self) -> EISMLModelDataPreparation:
        return self.data_preparation


    def get_training_tab(self) -> EISMLModelTraining:
        return self.training


    def get_testing_tab(self) -> EISMLModelTesting:
        return self.testing


    def get_application_tab(self) -> EISMLModelApplication:
        return self.application


    def get_parameter_values(self, as_str: bool) -> Dict[str, Any]:
        raise NotImplementedError("'get_parameter_values' needs to be defined in child class.")
