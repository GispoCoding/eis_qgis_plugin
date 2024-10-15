
from qgis.PyQt.QtWidgets import QComboBox, QSizePolicy, QStackedWidget, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.eda.exploratory_analysis.descriptive_statistics import EISWizardDescritiveStatistics

FORM_CLASS: QWidget = load_ui("eda/wizard_statistics.ui")


class EISWizardExploratoryAnalysis(QWidget, FORM_CLASS):

    algorithm_selection: QComboBox
    parameters_container: QStackedWidget

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.algorithm_selection.currentIndexChanged['int'].connect(self.parameters_container.setCurrentIndex)

        self.parameters_container.currentChanged.connect(self.resize_parameter_container)

        # Create pages for parameters
        self.pages = [
            EISWizardDescritiveStatistics(self),
        ]

        for i, page in enumerate(self.pages):
            self.parameters_container.insertWidget(i, page)



    def resize_parameter_container(self, index):
        """Resize the QStackedWidget that contains plot parameters according to the needed size."""
        widget = self.parameters_container.widget(index)
        if widget:
            self.parameters_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.parameters_container.setMinimumHeight(widget.height())