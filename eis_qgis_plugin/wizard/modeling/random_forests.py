from qgis import processing
from qgis.PyQt.QtWidgets import QComboBox, QSpinBox, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.model_template import EISModel, ModelType

FORM_CLASS: QWidget = load_ui("model/wizard_model_random_forests_2.ui")


class EISWizardRandomForests(EISModel, FORM_CLASS):
    """
    Class for random forest models.
    """
    n_estimators: QSpinBox
    criterion: QComboBox
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


    def set_tooltips(self):
        super().set_tooltips()

        n_estimators_tip = "The number of trees in the forest."
        self.n_estimators.setToolTip(n_estimators_tip)
        self.n_estimators_label.setToolTip(n_estimators_tip)

        criterion_tip =""  #TODO
        self.criterion.setToolTip(criterion_tip)
        self.criterion_label.setToolTip(criterion_tip)

        max_depth_tip = (
            "The maximum depth of the tree. If None, nodes are expanded until all leaves are pure or"
            " until all leaves contain less than min_samples_split samples."
        )
        self.max_depth.setToolTip(max_depth_tip)
        self.max_depth_label.setToolTip(max_depth_tip)

        verbose_tip = (
            "Specifies if modeling progress and performance should be printed."
            " 0 doesn't print, values 1 or above will produce prints."
        )
        self.verbose.setToolTip(verbose_tip)
        self.verbose_label.setToolTip(verbose_tip)

        random_state_tip = "Seed for random number generation."
        self.random_state.setToolTip(random_state_tip)
        self.random_state_label.setToolTip(random_state_tip)


    def initialize_classifier(self):
        """Initialize random forest classifier settings."""
        super().initialize_classifier()
        self.criterion.addItems(["gini", "entropy", "log_loss"])


    def initialize_regressor(self):
        """Initialize random forest regressor settings."""
        super().initialize_regressor()
        self.criterion.addItems(["squared_error", "absolute_error", "friedman_mse", "poisson"])


    def train_model(self, text_edit, progress_bar):
        """
        Train a random forest model.

        Runs the EIS random_forest_classifier or random_forest_regressor processing algorithm. Computation is
        done in EIS backend (EIS Toolkit).
        """
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

        # Testing
        from time import sleep
        for i in range(1, 101):
            progress_bar.setValue(i)
            if i % 10 == 0:
                text_edit.append(f"Progress: {i}%")
            sleep(0.05)
        text_edit.append("Finished!")
