from qgis import processing
from qgis.gui import QgsSpinBox
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.model_template import EISModel, ModelType

FORM_CLASS: QWidget = load_ui("model/wizard_model_logistic_regression_2.ui")


class EISWizardLogisticRegression(EISModel, FORM_CLASS):
    """
    Class for logistic regression.
    """
    penalty: QComboBox
    max_iter: QgsSpinBox
    solver: QComboBox
    verbose: QgsSpinBox
    random_state: QgsSpinBox


    def __init__(self, parent) -> None:
        self.parameter_box_collapse_effect = 170
        self.start_height = 591

        super().__init__(parent, ModelType.CLASSIFIER)

        super().initialize_classifier()


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
