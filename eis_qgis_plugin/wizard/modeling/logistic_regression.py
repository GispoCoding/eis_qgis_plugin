from qgis import processing
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QSpinBox,
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
    max_iter: QSpinBox
    solver: QComboBox
    verbose: QSpinBox
    random_state: QSpinBox


    def __init__(self, parent) -> None:
        self.parameter_box_collapse_effect = 170
        self.start_height = 591

        super().__init__(parent, ModelType.CLASSIFIER)

        super().initialize_classifier()


    def train_model(self):
        # Skeleton

        layers = self.get_training_layers()

        processing.run(
            "eis:logistic_regression",
            {
                'input_data': layers,
                'labels': self.y.layer(),

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
