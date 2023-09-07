from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialog,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.wizard.preprocess.wizard_preprocess import EISWizardPreprocess

FORM_CLASS: QDialog = load_ui("preprocess/settings.ui")

study_scales = ["regional", "camp", "deposit"]
mineral_systems = ["iocg", "Mineral system 2", "Mineral system 3"]

class EISWizardPreprocessSettings(QDialog, FORM_CLASS):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.main_layout = QVBoxLayout()
        self.layout_scale = QHBoxLayout()
        self.layout_system = QHBoxLayout()
        self.combobox_scale = QComboBox()
        self.combobox_system = QComboBox()
        self.select_button = QPushButton("Select")

        self.populate_comboboxes()
        
        self.layout_scale.addWidget(QLabel("Study scale:"))
        self.layout_scale.addWidget(self.combobox_scale)
        self.layout_system.addWidget(QLabel("Mineral System:"))
        self.layout_system.addWidget(self.combobox_system)

        self.main_layout.addLayout(self.layout_scale)
        self.main_layout.addLayout(self.layout_system)
        self.main_layout.addWidget(self.select_button)

        self.setLayout(self.main_layout)

        self.combobox_scale.setFixedWidth(150)
        self.combobox_system.setFixedWidth(150)

        self.select_button.clicked.connect(self.send_settings)



    def populate_comboboxes(self):
        self.combobox_scale.addItems(study_scales)
        self.combobox_system.addItems(mineral_systems)

    def send_settings(self):
        study_scale = self.combobox_scale.currentText()
        mineral_system = self.combobox_system.currentText()
        self.close()
        main_window = EISWizardPreprocess(study_scale, mineral_system)
        main_window.exec()