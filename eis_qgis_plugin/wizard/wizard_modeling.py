from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialog,
    QGroupBox,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QStackedWidget,
    QTabWidget,
    QTextEdit,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.gradient_boosting import EISWizardGradientBoosting
from eis_qgis_plugin.wizard.modeling.logistic_regression import EISWizardLogisticRegression
from eis_qgis_plugin.wizard.modeling.model_data_table import ModelDataTable
from eis_qgis_plugin.wizard.modeling.model_template import ModelType
from eis_qgis_plugin.wizard.modeling.random_forests import EISWizardRandomForests

FORM_CLASS: QDialog = load_ui("model/wizard_model_new_2.ui")


class EISWizardModeling(QWidget, FORM_CLASS):
    # table: QTableWidget
    model_selection: QComboBox
    model_parameters_container: QStackedWidget

    start_training_btn: QPushButton
    reset_btn: QPushButton

    model_output_tab: QTabWidget
    training_log: QTextEdit
    training_progress_bar: QProgressBar

    # Application
    application_data_groupbox: QGroupBox
    table_placeholder: QWidget
    test_radiobutton: QRadioButton
    predict_radiobutton: QRadioButton

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.model_selection.currentIndexChanged['int'].connect(self.model_parameters_container.setCurrentIndex)

        self.initialize_model_data_preparation()
        self.initialize_model_creation()
        self.initialize_model_application()

    def initialize_model_data_preparation(self):
        pass

    def initialize_model_creation(self):
        self.model_parameters_container.currentChanged.connect(self.resize_parameter_container)

        self.start_training_btn.clicked.connect(self.train_selected_model)
        self.reset_btn.clicked.connect(self.reset_selected_model)

        self.pages = [
            EISWizardLogisticRegression(self),
            EISWizardRandomForests(self, ModelType.CLASSIFIER),
            EISWizardRandomForests(self, ModelType.REGRESSOR),
            EISWizardGradientBoosting(self, ModelType.CLASSIFIER),
            EISWizardGradientBoosting(self, ModelType.REGRESSOR)
        ]

        for i, page in enumerate(self.pages):
            self.model_parameters_container.insertWidget(i, page)

        self.resize_parameter_container(0)

        # headers = ["Precision", "Recall", "Accuracy", "Support"]
        # self.table.setHorizontalHeaderLabels(headers)
        # self.table.setDisabled(True)
        # self.table.

        # self.layer_tree = QgsLayerTreeView()

        # WORKING?
        # root = QgsProject.instance().layerTreeRoot()
        # model = QgsLayerTreeModel(root)
        # view = QgsLayerTreeView()
        # view.setModel(model)
        # view.show()

        # Create pages for parameters

    def initialize_model_application(self):
        table = ModelDataTable(self)
        self.application_data_table_layout.addWidget(table)

        self.test_radiobutton.toggled.connect(lambda: self.application_mode_changed(self.test_radiobutton))
        self.predict_radiobutton.toggled.connect(lambda: self.application_mode_changed(self.predict_radiobutton))


    def application_mode_changed(self, btn):
        if self.test_radiobutton.isChecked():
            self.application_y_label.show()
            self.application_y.show()
            self.evaluation_metrics_groupbox.show()
        else:
            self.application_y_label.hide()
            self.application_y.hide()
            self.evaluation_metrics_groupbox.hide()


    def train_selected_model(self):
        """Call the run method of the selected model."""
        page = self.pages[self.model_parameters_container.currentIndex()]
        result = page.train_model(self.training_log, self.training_progress_bar)
        if result:
            page.show_output()  # TODO


    def reset_selected_model(self):
        """Reset parameters of the selected model."""
        page = self.pages[self.model_parameters_container.currentIndex()]
        page.reset()


    def resize_parameter_container(self, index):
        """Resize the QStackedWidget that contains model parameters according to the needed size."""
        widget = self.model_parameters_container.widget(index)
        if widget:
            self.model_parameters_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.model_parameters_container.setMinimumHeight(widget.current_height)
            widget.setMaximumHeight(widget.current_height)
            widget.setMinimumHeight(widget.current_height)
