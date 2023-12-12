from qgis.gui import QgsCheckableComboBox, QgsFileWidget, QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QSpinBox,
    QTableWidget,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.model_template import EISModel, ModelType

FORM_CLASS: QWidget = load_ui("model/wizard_model_random_forests_2.ui")


class EISWizardRandomForests(EISModel, FORM_CLASS):
    """
    Class for random forest models.
    """
    X: QgsMapLayerComboBox
    y: QgsMapLayerComboBox

    n_estimators: QComboBox
    max_depth: QSpinBox
    verbose: QSpinBox
    random_state: QSpinBox

    model_save_path: QgsFileWidget

    validation_method: QComboBox
    split_size: QDoubleSpinBox
    cv: QSpinBox
    validation_metric: QgsCheckableComboBox

    results_table: QTableWidget

    def __init__(self, parent, model_type) -> None:
        self.parameter_box_collapse_effect = 170
        self.start_height = 591
        self.model_type = model_type  # Classifier or regressor

        super().__init__(parent, model_type)

        if model_type == ModelType.CLASSIFIER:
            self.initialize_classifier()
        elif model_type == ModelType.REGRESSOR:
            self.initialize_regressor()

        # self.train_pb.clicked.connect(self.on_train_button_clicked)

    # def on_train_button_clicked(self):
    #     self.model_save_path.filePath()
    #     self.read_model_parameters()
    #     self.read_validation_settings()
    #     # Train the model with above parameters and settings
    #     self.populate_table()

    def initialize_classifier(self):
        super().initialize_classifier()
        self.criterion = ["gini", "entropy", "log_loss"]

    def initialize_regressor(self):
        super().initialize_regressor()
        self.criterion = ["squared_error", "absolute_error", "friedman_mse", "poisson"]

    def run_model(self, text_edit, progress_bar):
        from time import sleep
        for i in range(1, 101):
            progress_bar.setValue(i)
            if i % 10 == 0:
                text_edit.append(f"Progress: {i}%")
            sleep(0.05)
        text_edit.append("Finished!")


    def populate_table(self):
        self.results_table.clear()
        headers = self.metrics.checkedItems()

        self.results_table.setRowCount(1)
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        # TODO: Populate table with train results

    def read_model_parameters(self):
        n_estimators = self.n_estimators.currentText()
        max_depth = self.max_depth.value()
        verbose = self.verbose.value()
        random_state = self.random_state.value()
        return [n_estimators, max_depth, verbose, random_state]

    def read_validation_settings(self):
        validation_method = self.validation_method.currentText()
        metrics = self.metrics.checkedItems()
        split_size = self.split_size.value()
        cv_folds = self.cv.value()
        return [validation_method, metrics, split_size, cv_folds]
