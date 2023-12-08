from qgis.gui import QgsCheckableComboBox, QgsFileWidget, QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.model_template import EISModel

FORM_CLASS: QWidget = load_ui("model/wizard_model_logistic_regression.ui")


class EISWizardLogisticRegression(EISModel, FORM_CLASS):
    """
    Class for logistic regression.
    """

    penalty_cb: QComboBox
    max_iter_sb: QSpinBox
    solver_cb: QComboBox
    verbose_sb: QSpinBox
    random_state_sb: QSpinBox

    model_save_path: QgsFileWidget

    X_cb: QgsMapLayerComboBox
    y_cb: QgsMapLayerComboBox

    validation_method_cb: QComboBox
    metrics_cb: QgsCheckableComboBox
    split_size_sb: QDoubleSpinBox
    cv_sb: QSpinBox

    train_pb: QPushButton
    results_table: QTableWidget

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.train_pb.clicked.connect(self.on_train_button_clicked)

    def on_train_button_clicked(self):
        self.model_save_path.filePath()
        self.read_model_parameters()
        self.read_validation_settings()
        # Train the model with above parameters and settings
        self.populate_table()

    def populate_table(self):
        self.results_table.clear()
        headers = self.metrics_cb.checkedItems()

        self.results_table.setRowCount(1)
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        # TODO: Populate table with train results

    def read_model_parameters(self):
        penalty = self.penalty_cb.currentText()
        max_iter = self.max_iter_sb.value()
        solver = self.solver_cb.currentText()
        verbose = self.verbose_sb.value()
        random_state = self.random_state_sb.value()
        return [penalty, max_iter, solver, verbose, random_state]

    def read_validation_settings(self):
        validation_method = self.validation_method_cb.currentText()
        metrics = self.metrics_cb.checkedItems()
        split_size = self.split_size_sb.value()
        cv_folds = self.cv_sb.value()
        return [validation_method, metrics, split_size, cv_folds]

    def read_data(self):
        # Miten data annetaan? Onko 1 vai useampi taso?
        self.X_cb.currentField()
        self.y_cb.currentField()
