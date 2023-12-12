from qgis import processing
from qgis.PyQt.QtWidgets import (
    QSpinBox,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.model_template import EISModel, ModelType

FORM_CLASS: QWidget = load_ui("model/wizard_model_random_forests_2.ui")


class EISWizardRandomForests(EISModel, FORM_CLASS):
    """
    Class for random forest models.
    """
    n_estimators: QSpinBox
    max_depth: QSpinBox
    verbose: QSpinBox
    random_state: QSpinBox

    def __init__(self, parent, model_type) -> None:
        self.parameter_box_collapse_effect = 170
        self.start_height = 591
        self.model_type = model_type  # Classifier or regressor

        super().__init__(parent, model_type)

        if model_type == ModelType.CLASSIFIER:
            self.initialize_classifier()
        elif model_type == ModelType.REGRESSOR:
            self.initialize_regressor()


    def initialize_classifier(self):
        super().initialize_classifier()
        self.criterion = ["gini", "entropy", "log_loss"]


    def initialize_regressor(self):
        super().initialize_regressor()
        self.criterion = ["squared_error", "absolute_error", "friedman_mse", "poisson"]


    def train_model(self, text_edit, progress_bar):
        # Skeleton

        alg = "eis:random_forest_" + "classifier" if self.model_type == ModelType.CLASSIFIER else "regressor"
        layers = self.get_training_layers()

        processing.run(
            alg,
            {
                'input_data': layers,
                'labels': self.y.layer(),

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

        from time import sleep
        for i in range(1, 101):
            progress_bar.setValue(i)
            if i % 10 == 0:
                text_edit.append(f"Progress: {i}%")
            sleep(0.05)
        text_edit.append("Finished!")
