from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialog,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QTabWidget,
    QTextEdit,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.modeling.gradient_boosting import EISWizardGradientBoosting
from eis_qgis_plugin.wizard.modeling.logistic_regression import EISWizardLogisticRegression
from eis_qgis_plugin.wizard.modeling.model_template import ModelType
from eis_qgis_plugin.wizard.modeling.random_forests import EISWizardRandomForests

FORM_CLASS: QDialog = load_ui("model/wizard_model_new.ui")


class EISWizardModeling(QWidget, FORM_CLASS):
    # table: QTableWidget
    model_selection: QComboBox
    model_parameters_container: QStackedWidget

    start_training_btn: QPushButton
    reset_btn: QPushButton

    model_output_tab: QTabWidget
    training_log: QTextEdit
    training_progress_bar: QProgressBar

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.model_selection.currentIndexChanged['int'].connect(self.model_parameters_container.setCurrentIndex)

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

        print(self.model_parameters_container.height())
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
