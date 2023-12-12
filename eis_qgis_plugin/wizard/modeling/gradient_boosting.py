from qgis import processing
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QSpinBox,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.model_template import EISModel, ModelType

FORM_CLASS: QWidget = load_ui("model/wizard_model_gradient_boosting_2.ui")


class EISWizardGradientBoosting(EISModel, FORM_CLASS):
    """
    Class for gradient boosting models.
    """
    loss: QComboBox
    learning_rate: QDoubleSpinBox
    n_estimators: QSpinBox
    max_depth: QSpinBox
    verbose: QSpinBox
    random_state: QSpinBox


    def __init__(self, parent, model_type) -> None:
        self.parameter_box_collapse_effect = 201
        self.start_height = 628

        super().__init__(parent, model_type)

        if model_type == ModelType.CLASSIFIER:
            self.initialize_classifier()
        elif model_type == ModelType.REGRESSOR:
            self.initialize_regressor()


    def initialize_classifier(self):
        super().initialize_classifier()
        self.loss.addItems(["log_loss", "exponential"])


    def initialize_regressor(self):
        super().initialize_regressor()
        self.loss.addItems(["squared_error", "absolute_error", "huber", "quantile"])


    def train_model(self, text_edit, progress_bar):
        # Skeleton

        alg = "eis:gradient_boosting" + "classifier" if self.model_type == ModelType.CLASSIFIER else "regressor"
        layers = self.get_training_layers()

        processing.run(
            alg,
            {
                'input_data': layers,
                'labels': self.y.layer(),

                'learning_rate': self.learning_rate.value(),
                'loss': self.loss.currentText(),
                'n_estimators': self.n_estimators.value(),
                'max_depth': self.max_depth.value(),
                'verbose': self.verbose.value(),
                'random_state': self.random_state.value(),
                'model_save_path': self.model_save_path.filePath(),

                'validation_method': self.validation_method.currentText(),
                'split_size': self.split_size.value(),
                'cv': self.cv_folds.value(),
                'validation_metric': self.validation_metric.currentText()
            }
        )

        # LOG TEST
        from time import sleep
        example_log_output = [
            "Iter       Train Loss   Remaining Time",
            "1           0.9204            0.12s",
            "2           0.7818            0.12s",
            "3           0.6700            0.12s",
            "4           0.5786            0.11s",
            "5           0.5028            0.11s",
            "6           0.4393            0.11s",
            "7           0.3856            0.11s",
            "8           0.3398            0.11s",
            "9           0.2977            0.10s",
            "10           0.2616            0.10s",
            "20           0.0806            0.09s",
            "30           0.0314            0.08s",
            "40           0.0142            0.07s",
            "50           0.0071            0.06s",
            "60           0.0039            0.04s",
            "70           0.0021            0.03s",
            "80           0.0011            0.02s",
            "90           0.0006            0.01s",
            "100           0.0003            0.00s"
        ]
        estimators = self.n_estimators.value()
        for line in example_log_output:
            sleep(0.1)
            text_edit.append(line)
            iteration = line.split()[0]
            try:
                number = int(iteration)
                progress_bar.setValue(int(number / estimators * 100))
            except ValueError:
                pass

        text_edit.append("\n Training finished!")
