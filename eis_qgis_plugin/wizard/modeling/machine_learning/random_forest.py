from typing import Any, Dict

from qgis.gui import QgsSpinBox
from qgis.PyQt.QtWidgets import QComboBox, QLabel

from eis_qgis_plugin.wizard.modeling.machine_learning.ml_model import EISMLModel, ModelType


class EISWizardRandomForest(EISMLModel):
    """
    Class for random forest models.
    """

    def __init__(self, parent, model_type) -> None:
        super().__init__(parent, model_type)
        
        self.add_model_parameters()
        self.add_general_model_parameters()

        self.model_type = model_type  # Classifier or regressor
        if model_type == ModelType.CLASSIFIER:
            self.initialize_classifier()
        elif model_type == ModelType.REGRESSOR:
            self.initialize_regressor()


    def add_model_parameters(self):
        """Add parameter widgets for Random Forest model."""
        self.n_estimators_label = QLabel()
        self.n_estimators_label.setText("N estimators")
        self.n_estimators = QgsSpinBox()
        self.n_estimators.setMinimum(1)
        self.n_estimators.setMaximum(1000)
        self.n_estimators.setValue(100)
        self.train_parameter_box.layout().addRow(self.n_estimators_label, self.n_estimators)

        self.criterion_label = QLabel()
        self.criterion_label.setText("Criterion")
        self.criterion = QComboBox()
        
        self.train_parameter_box.layout().addRow(self.criterion_label, self.criterion)

        self.max_depth_label = QLabel()
        self.max_depth_label.setText("Max depth")
        self.max_depth = QgsSpinBox()
        self.max_depth.setMinimum(0)
        self.max_depth.setMaximum(1000)
        self.max_depth.setValue(3)
        self.train_parameter_box.layout().addRow(self.max_depth_label, self.max_depth)


    def initialize_classifier(self):
        """Initialize random forest classifier settings."""
        self.name = "Random forest classifier"
        self.alg_name = "eis:random_forest_classifier_train"
        super().initialize_classifier()
        self.criterion.addItems(["gini", "entropy", "log_loss"])


    def initialize_regressor(self):
        """Initialize random forest regressor settings."""
        self.name = "Random forest regressor"
        self.alg_name = "eis:random_forest_classifier_train"
        super().initialize_regressor()
        self.criterion.addItems(["squared_error", "absolute_error", "friedman_mse", "poisson"])


    def get_parameter_values(self) -> Dict[str, Any]:
        return {
            'n_estimators': self.n_estimators.value(),
            'criterion': self.criterion.currentIndex(),
            'max_depth': self.max_depth.value()
        }
    

    def reset_parameters(self):
        """Reset random forest parameters to defaults."""
        super().reset_parameters()

        self.n_estimators.setValue(100)
        self.criterion.setCurrentIndex(0)
        self.max_depth.setValue(-1)


    def set_tooltips(self):
        """Set tooltips for random forest parameters."""
        super().set_tooltips()

        n_estimators_tip = "The number of trees in the forest."
        self.n_estimators.setToolTip(n_estimators_tip)
        self.n_estimators_label.setToolTip(n_estimators_tip)

        criterion_tip = "" # TODO
        self.criterion.setToolTip(criterion_tip)
        self.criterion_label.setToolTip(criterion_tip)

        max_depth_tip = (
            "The maximum depth of the tree. If None, nodes are expanded until all leaves are pure or"
            " until all leaves contain less than min_samples_split samples."
        )
        self.max_depth.setToolTip(max_depth_tip)
        self.max_depth_label.setToolTip(max_depth_tip)
