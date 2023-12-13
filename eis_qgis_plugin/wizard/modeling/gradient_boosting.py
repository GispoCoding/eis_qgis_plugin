from qgis import processing
from qgis.gui import QgsDoubleSpinBox, QgsSpinBox
from qgis.PyQt.QtWidgets import QComboBox, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.model_template import EISModel, ModelType

FORM_CLASS: QWidget = load_ui("model/wizard_model_gradient_boosting_2.ui")


class EISWizardGradientBoosting(EISModel, FORM_CLASS):
    """
    Class for gradient boosting models.
    """
    loss: QComboBox
    learning_rate: QgsDoubleSpinBox
    n_estimators: QgsSpinBox
    max_depth: QgsSpinBox
    subsample: QgsDoubleSpinBox
    verbose: QgsSpinBox
    random_state: QgsSpinBox


    def __init__(self, parent, model_type) -> None:
        self.parameter_box_collapse_effect = 232
        self.start_height = 653

        super().__init__(parent, model_type)

        if model_type == ModelType.CLASSIFIER:
            self.initialize_classifier()
        elif model_type == ModelType.REGRESSOR:
            self.initialize_regressor()


    def initialize_classifier(self):
        """Initialize gradient boosting classifier settings."""
        super().initialize_classifier()
        self.loss.addItems(["log_loss", "exponential"])


    def initialize_regressor(self):
        """Initialize gradient boosting regressor settings."""
        super().initialize_regressor()
        self.loss.addItems(["squared_error", "absolute_error", "huber", "quantile"])


    def set_tooltips(self):
        """Set tooltips for gradient boosting parameters."""
        super().set_tooltips()

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

        verbose_tip = (
            "Specifies if modeling progress and performance should be printed. 0 doesn't print,"
            " 1 prints once in a while depending on the number of tress, 2 or above will print for every tree."
        )
        self.verbose.setToolTip(verbose_tip)
        self.verbose_label.setToolTip(verbose_tip)

        random_state_tip = "Seed for random number generation."
        self.random_state.setToolTip(random_state_tip)
        self.random_state_label.setToolTip(random_state_tip)


    def train_model(self, text_edit, progress_bar):
        """
        Train a gradient boosting model.

        Runs the EIS gradient_boosting_classifier or gradient_boosting_regressor processing algorithm. Computation is
        done in EIS backend (EIS Toolkit).
        """
        # Skeleton

        alg = "eis:gradient_boosting" + "classifier" if self.model_type == ModelType.CLASSIFIER else "regressor"
        layers = self.get_training_layers()

        if False:
            processing.run(
                alg,
                {
                    'input_data': layers,
                    'labels': self.y.currentLayer(),

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

        # Testing
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


    def reset(self):
        """Reset gradient boosting parameters to defaults."""
        super().reset()

        self.loss.setCurrentIndex(0)
        self.learning_rate.setValue(0.1)
        self.n_estimators.setValue(100)
        self.max_depth.setValue(3)
        self.subsample.setValue(1)
        self.verbose.setValue(0)
        self.random_state.setValue(-1)
