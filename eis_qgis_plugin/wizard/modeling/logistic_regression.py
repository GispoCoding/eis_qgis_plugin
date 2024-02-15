from qgis import processing
from qgis.gui import QgsSpinBox
from qgis.PyQt.QtWidgets import QComboBox, QLabel

from eis_qgis_plugin.wizard.modeling.ml_model_template import EISModel, ModelType


class EISWizardLogisticRegression(EISModel):
    """
    Class for logistic regression.
    """

    def __init__(self, parent) -> None:
        super().__init__(parent, ModelType.CLASSIFIER)

        self.add_model_parameters()
        self.add_general_model_parameters()

        super().initialize_classifier()

    
    def add_model_parameters(self):
        """Add parameter widgets for Logistic Regression model."""
        self.penalty_label = QLabel()
        self.penalty_label.setText("Penalty")
        self.penalty = QComboBox()
        self.penalty.addItems(["l2", "l1", "elasicnet", "None"])
        self.train_parameter_box.layout().addRow(self.penalty_label, self.penalty)

        self.max_iter_label = QLabel()
        self.max_iter_label.setText("Max iter")
        self.max_iter = QgsSpinBox()
        self.max_iter.setMinimum(1)
        self.max_iter.setMaximum(1000)
        self.max_iter.setValue(100)
        self.train_parameter_box.layout().addRow(self.max_iter_label, self.max_iter)

        self.solver_label = QLabel()
        self.solver_label.setText("Solver")
        self.solver = QComboBox()
        self.solver.addItems(["lbfgs", "liblinear", "newton-cg", "newton-cholesky", "sag", "saga"])
        self.train_parameter_box.layout().addRow(self.solver_label, self.solver)


    def set_tooltips(self):
        """Set tooltips for logistic regression parameters."""
        super().set_tooltips()

        penalty_tip = "Specifies the norm of the penalty."
        self.penalty.setToolTip(penalty_tip)
        self.penalty_label.setToolTip(penalty_tip)

        max_iter_tip = "Maximum number of iterations taken for the solvers to converge."
        self.max_iter.setToolTip(max_iter_tip)
        self.max_iter_label.setToolTip(max_iter_tip)

        solver_tip = "Algorithm to use in the optimization problem."
        self.solver.setToolTip(solver_tip)
        self.solver_label.setToolTip(solver_tip)

        verbose_tip = (
            "Specifies if modeling progress and performance should be printed."
            " 0 doesn't print, values 1 or above will produce prints."
        )
        self.verbose.setToolTip(verbose_tip)
        self.verbose_label.setToolTip(verbose_tip)

        random_state_tip = "Seed for random number generation."
        self.random_state.setToolTip(random_state_tip)
        self.random_state_label.setToolTip(random_state_tip)


    def train_model(self, text_edit, progress_bar):
        """
        Train a logistic regression model.

        Runs the EIS logistic_regression processing algorithm. Computation is done in EIS backend (EIS Toolkit).
        """
        # Skeleton

        layers = self.get_training_layers()

        if False:
            processing.run(
                "eis:logistic_regression",
                {
                    'input_data': layers,
                    'labels': self.y.currentLayer(),

                    'penalty': self.penalty.currentText(),
                    'max_iter': self.max_iter.value(),
                    'solver': self.solver.currentText(),
                    'verbose': self.verbose.value(),
                    'random_state': self.random_state.value(),
                    'model_save_path': self.model_save_path.filePath(),

                    'validation_method': self.validation_method.currentText(),
                    'split_size': self.split_size.value(),
                    'cv': self.cv_folds.value(),
                    'validation_metric': self.validation_metric.currentText()
                }
            )

        pass


    def reset(self):
        """Reset logistic regression parameters to defaults."""
        super().reset()

        self.penalty.setCurrentIndex(0)
        self.max_iter.setValue(100)
        self.solver.setCurrentIndex(0)
        self.verbose.setValue(0)
        self.random_state.setValue(-1)
