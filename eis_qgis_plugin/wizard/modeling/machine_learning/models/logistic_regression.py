from typing import Any, Dict

from qgis.gui import QgsSpinBox
from qgis.PyQt.QtWidgets import QComboBox, QLabel

from eis_qgis_plugin.wizard.modeling.machine_learning.ml_model_main import EISMLModel
from eis_qgis_plugin.wizard.modeling.model_utils import ModelType


class EISWizardLogisticRegression(EISMLModel):
    """
    Class for logistic regression.
    """

    def __init__(self, parent) -> None:
        self.name = "Logistic regression"
        self.alg_name = "eis:logistic_regression_train"

        super().__init__(parent, self.name, ModelType.CLASSIFIER)

        self.training_tab = super().get_training_tab()
        self.training_tab.add_common_parameters()
        self.add_model_parameters()

        self.training_tab.initialize_classifier()

    
    def add_model_parameters(self):
        """Add parameter widgets for Logistic Regression model."""
        self.penalty_label = QLabel()
        self.penalty_label.setText("Penalty")
        self.penalty = QComboBox()
        self.penalty.addItems(["l2", "l1", "elasicnet", "None"])
        self.training_tab.add_parameter_row(self.penalty_label, self.penalty)

        self.max_iter_label = QLabel()
        self.max_iter_label.setText("Max iter")
        self.max_iter = QgsSpinBox()
        self.max_iter.setMinimum(1)
        self.max_iter.setMaximum(1000)
        self.max_iter.setValue(100)
        self.training_tab.add_parameter_row(self.max_iter_label, self.max_iter)

        self.solver_label = QLabel()
        self.solver_label.setText("Solver")
        self.solver = QComboBox()
        self.solver.addItems(["lbfgs", "liblinear", "newton-cg", "newton-cholesky", "sag", "saga"])
        self.training_tab.add_parameter_row(self.solver_label, self.solver)


    def get_parameter_values(self) -> Dict[str, Any]:
        return {
            'penalty': self.penalty.currentIndex(),
            'max_iter': self.max_iter.value(),
            'solver': self.solver.currentIndex()
        }


    def reset_parameters(self):
        """Reset logistic regression parameters to defaults."""
        self.training_tab.reset_parameters()

        self.penalty.setCurrentIndex(0)
        self.max_iter.setValue(100)
        self.solver.setCurrentIndex(0)


    def set_tooltips(self):
        """Set tooltips for logistic regression parameters."""
        self.training_tab.set_tooltips()

        penalty_tip = "Specifies the norm of the penalty."
        self.penalty.setToolTip(penalty_tip)
        self.penalty_label.setToolTip(penalty_tip)

        max_iter_tip = "Maximum number of iterations taken for the solvers to converge."
        self.max_iter.setToolTip(max_iter_tip)
        self.max_iter_label.setToolTip(max_iter_tip)

        solver_tip = "Algorithm to use in the optimization problem."
        self.solver.setToolTip(solver_tip)
        self.solver_label.setToolTip(solver_tip)
