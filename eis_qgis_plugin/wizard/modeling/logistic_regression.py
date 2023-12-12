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

FORM_CLASS: QWidget = load_ui("model/wizard_model_logistic_regression_2.ui")


class EISWizardLogisticRegression(EISModel, FORM_CLASS):
    """
    Class for logistic regression.
    """
    X: QgsMapLayerComboBox
    y: QgsMapLayerComboBox

    penalty: QComboBox
    max_iter: QSpinBox
    solver: QComboBox
    verbose: QSpinBox
    random_state: QSpinBox

    model_save_path: QgsFileWidget

    validation_method: QComboBox
    split_size: QDoubleSpinBox
    cv: QSpinBox
    validation_metric: QgsCheckableComboBox

    results_table: QTableWidget

    def __init__(self, parent) -> None:
        self.parameter_box_collapse_effect = 170
        self.start_height = 591

        super().__init__(parent, ModelType.CLASSIFIER)

        super().initialize_classifier()

    #     self.train_pb.clicked.connect(self.on_train_button_clicked)

    # def on_train_button_clicked(self):
    #     self.model_save_path.filePath()
    #     self.read_model_parameters()
    #     self.read_validation_settings()
    #     # Train the model with above parameters and settings
    #     self.populate_table()

    def run_model(self):
        pass

    def populate_table(self):
        self.results_table.clear()
        headers = self.metrics.checkedItems()

        self.results_table.setRowCount(1)
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        # TODO: Populate table with train results

    def read_model_parameters(self):
        penalty = self.penalty.currentText()
        max_iter = self.max_iter.value()
        solver = self.solver.currentText()
        verbose = self.verbose.value()
        random_state = self.random_state.value()
        return [penalty, max_iter, solver, verbose, random_state]

    def read_validation_settings(self):
        validation_method = self.validation_method.currentText()
        metrics = self.metrics.checkedItems()
        split_size = self.split_size.value()
        cv_folds = self.cv.value()
        return [validation_method, metrics, split_size, cv_folds]

    def read_data(self):
        # Miten data annetaan? Onko 1 vai useampi taso?
        self.X.currentField()
        self.y.currentField()
