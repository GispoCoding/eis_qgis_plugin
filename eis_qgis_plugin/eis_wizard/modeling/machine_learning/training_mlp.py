from typing import Any, Dict

from qgis.gui import QgsSpinBox
from qgis.PyQt.QtWidgets import QLabel, QPushButton

from eis_qgis_plugin.eis_wizard.modeling.machine_learning.training import EISMLModelTraining


class EISMLModelTrainingMLP(EISMLModelTraining):

    def __init__(self, parent, model_main) -> None:
        super().__init__(parent, model_main)

        self.reset_training_parameters_btn: QPushButton

        self.validation_method_label.deleteLater()
        self.validation_method.deleteLater()
        self.cv_folds_label.deleteLater()
        self.cv_folds.deleteLater()

        self.reset_training_parameters_btn.clicked.connect(self.reset_parameters)


    def add_common_parameters(self):
        """Add common parameters to the parameter box."""
        self.random_state_label = QLabel()
        self.random_state_label.setText("Random state")
        self.random_state = QgsSpinBox()
        self.random_state.setMinimum(-1)
        self.random_state.setMaximum(10000)
        self.random_state.setValue(-1)
        self.random_state.setSpecialValueText("None (random)")
        self.add_parameter_row(self.random_state_label, self.random_state)
       

    def get_common_parameter_values(self) -> Dict[str, Any]:
        return {
            "random_state": None if self.random_state.value() == -1 else self.random_state.value()
        }


    def get_validation_settings(self, as_str: bool = False) -> Dict[str, Any]:
        return {
            "validation_split": self.split_size.value() / 100,
            "validation_metrics": self.validation_metrics.checkedItems() if as_str else
                [self.model_main.get_valid_metrics().index(elem) for elem in self.validation_metrics.checkedItems()]
        }
    

    def reset_parameters(self):
        """Reset common and validation parameters to defaults."""
        self.random_state.setValue(-1)

        self.split_size.setValue(20)
        self.add_validation_metrics()

        self.model_main.reset_parameters()


    def set_tooltips(self):
        """Set tooltips for the common and validation parameters."""
        evidence_data_tooltip = "Evidence layers for training the model."
        self.train_evidence_data.setToolTip(evidence_data_tooltip)
        self.train_evidence_data_box.setToolTip(evidence_data_tooltip)

        label_data_tooltip = "Layer with target labels for training."
        self.train_label_data.setToolTip(label_data_tooltip)
        self.train_label_data_box.setToolTip(label_data_tooltip)

        random_state_tip = "Seed for random number generation."
        self.random_state.setToolTip(random_state_tip)
        self.random_state_label.setToolTip(random_state_tip)

        split_size_tip = "Fraction of the dataset to be used as validation data (rest is used for training)."
        self.split_size.setToolTip(split_size_tip)
        self.split_size_label.setToolTip(split_size_tip)

        validation_metric_tip = "Metrics to use for scoring in validation."
        self.validation_metrics.setToolTip(validation_metric_tip)
        self.validation_metrics_label.setToolTip(validation_metric_tip)
