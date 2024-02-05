from qgis import processing
from qgis.gui import QgsSpinBox
from qgis.PyQt.QtWidgets import QComboBox, QLabel

from eis_qgis_plugin.wizard.modeling.ml_model_template import EISModel, ModelType


class EISWizardRandomForest(EISModel):
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

        if False:
            processing.run(
                alg,
                {
                    'input_data': layers,
                    'labels': self.y.currentLayer(),

                    'n_estimators': self.n_estimators.value(),
                    'criterion': self.criterion.currentText(),
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


    def reset(self):
        """Reset random forest parameters to defaults."""
        super().reset()

        self.n_estimators.setValue(0)
        self.criterion.setCurrentIndex(0)
        self.max_depth.setValue(3)
        self.verbose.setValue(0)
        self.random_state.setValue(-1)
