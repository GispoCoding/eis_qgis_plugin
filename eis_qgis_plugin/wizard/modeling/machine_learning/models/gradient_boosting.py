from typing import Any, Dict

from qgis.gui import QgsDoubleSpinBox, QgsSpinBox
from qgis.PyQt.QtWidgets import QComboBox, QLabel

from eis_qgis_plugin.wizard.modeling.machine_learning.ml_model_main import EISMLModel
from eis_qgis_plugin.wizard.modeling.model_utils import ModelKind


class EISWizardGradientBoosting(EISMLModel):
    """
    Class for gradient boosting models.
    """

    def __init__(self, parent, model_kind) -> None:
        self.model_kind = model_kind
        self.model_type = "Gradient boosting " + ("classifier" if model_kind == ModelKind.CLASSIFIER else "regressor")

        super().__init__(parent, self.model_type)

        self.training_tab = super().get_training_tab()
        self.training_tab.add_common_parameters()
        self.add_model_parameters()

        if model_kind == ModelKind.CLASSIFIER:
            self.initialize_classifier()
        elif model_kind == ModelKind.REGRESSOR:
            self.initialize_regressor()


    def add_model_parameters(self):
        """Add parameter widgets for Gradient Boosting model."""
        self.loss_label = QLabel()
        self.loss_label.setText("Loss")
        self.loss = QComboBox()
        self.loss.addItems([])
        self.training_tab.add_parameter_row(self.loss_label, self.loss)

        self.learning_rate_label = QLabel()
        self.learning_rate_label.setText("Learning rate")
        self.learning_rate = QgsDoubleSpinBox()
        self.learning_rate.setMinimum(0.01)
        self.learning_rate.setMaximum(99.99)
        self.learning_rate.setValue(0.1)
        self.training_tab.add_parameter_row(self.learning_rate_label, self.learning_rate)

        self.n_estimators_label = QLabel()
        self.n_estimators_label.setText("N estimators")
        self.n_estimators = QgsSpinBox()
        self.n_estimators.setMinimum(1)
        self.n_estimators.setMaximum(1000)
        self.n_estimators.setValue(100)
        self.training_tab.add_parameter_row(self.n_estimators_label, self.n_estimators)

        self.max_depth_label = QLabel()
        self.max_depth_label.setText("Max depth")
        self.max_depth = QgsSpinBox()
        self.max_depth.setMinimum(0)
        self.max_depth.setMaximum(1000)
        self.max_depth.setValue(3)
        self.training_tab.add_parameter_row(self.max_depth_label, self.max_depth)

        self.subsample_label = QLabel()
        self.subsample_label.setText("Subsample")
        self.subsample = QgsDoubleSpinBox()
        self.subsample.setMinimum(0.01)
        self.subsample.setMaximum(1.0)
        self.subsample.setValue(1.0)
        self.subsample.setDecimals(2)
        self.training_tab.add_parameter_row(self.subsample_label, self.subsample)


    def initialize_classifier(self):
        """Initialize gradient boosting classifier settings."""
        self.alg_name = "eis:gradient_boosting_classifier_train"
        self.training_tab.initialize_classifier()
        self.loss.addItems(["log_loss", "exponential"])


    def initialize_regressor(self):
        """Initialize gradient boosting regressor settings."""
        self.alg_name = "eis:gradient_boosting_regressor_train"
        self.training_tab.initialize_regressor()
        self.loss.addItems(["squared_error", "absolute_error", "huber", "quantile"])


    def get_parameter_values(self, as_str: bool = False) -> Dict[str, Any]:
        return {
            'learning_rate': self.learning_rate.value(),
            'loss': self.loss.currentText() if as_str else self.loss.currentIndex(),
            'n_estimators': self.n_estimators.value(),
            'max_depth': self.max_depth.value()
        }
    

    def reset_parameters(self):
        """Reset gradient boosting parameters to defaults."""
        self.training_tab.reset_parameters()

        self.loss.setCurrentIndex(0)
        self.learning_rate.setValue(0.1)
        self.n_estimators.setValue(100)
        self.max_depth.setValue(3)
        self.subsample.setValue(1)


    def set_tooltips(self):
        """Set tooltips for gradient boosting parameters."""
        self.training_tab.set_tooltips()

        loss_tip = "The loss function to be optimized."
        self.loss.setToolTip(loss_tip)
        self.loss_label.setToolTip(loss_tip)

        learning_rate_tip = "Shrinks the contribution of each tree."
        self.learning_rate.setToolTip(learning_rate_tip)
        self.learning_rate_label.setToolTip(learning_rate_tip)

        n_estimators_tip = (
            "The number of boosting stages to run. Gradient boosting is fairly robust to over-fitting"
            " so a large number can result in better performance."
        )
        self.n_estimators.setToolTip(n_estimators_tip)
        self.n_estimators_label.setToolTip(n_estimators_tip)

        max_depth_tip = (
            "Maximum depth of the individual regression estimators. The maximum depth limits the number"
            " of nodes in the tree. If None, nodes are expanded until all leaves"
            " are pure or until all leaves contain less than min_samples_split samples."
        )
        self.max_depth.setToolTip(max_depth_tip)
        self.max_depth_label.setToolTip(max_depth_tip)

        subsample_tip = (
            "The fraction of samples to be used for fitting the individual base learners."
            " If smaller than 1.0 this results in Stochastic Gradient Boosting. Subsample interacts with the"
            " parameter n_estimators."
            " Choosing subsample < 1.0 leads to a reduction of variance and an increase in bias."
        )
        self.subsample.setToolTip(subsample_tip)
        self.subsample_label.setToolTip(subsample_tip)

        # Override common verbose tooltip for Gradient boosting models
        verbose_tip = (
            "Specifies if modeling progress and performance should be printed. 0 doesn't print,"
            " 1 prints once in a while depending on the number of tress, 2 or above will print for every tree."
        )
        self.verbose.setToolTip(verbose_tip)
        self.verbose_label.setToolTip(verbose_tip)
