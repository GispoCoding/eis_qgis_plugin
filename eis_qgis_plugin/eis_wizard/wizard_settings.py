from qgis.core import QgsMapLayerProxyModel
from qgis.gui import QgsColorButton, QgsColorRampButton, QgsMapLayerComboBox
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QCheckBox, QComboBox, QDialog, QPushButton, QTabWidget, QVBoxLayout, QWidget
from qgis.utils import iface

from eis_qgis_plugin.eis_wizard.wizard_eis_toolkit_conf import EISWizardToolkitConfiguration
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.settings_manager import EISSettingsManager

FORM_CLASS: QDialog = load_ui("wizard_settings.ui")


class EISWizardSettings(QWidget, FORM_CLASS):

    minimal_menu_setting_changed = pyqtSignal(bool)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # DECLARE TYPES
        self.settings_tabs: QTabWidget

        self.default_base_raster: QgsMapLayerComboBox
        self.dock_wizard_selection: QCheckBox
        self.minimal_menu_selection: QCheckBox
        self.layer_group_selection: QCheckBox

        self.color_ramp_layout: QVBoxLayout
        self.categorical_palette_selection: QComboBox
        self.continuous_palette_selection: QComboBox
        self.default_color_selection: QgsColorButton

        self.save_settings_btn: QPushButton
        self.reset_settings_btn: QPushButton

        # Connect signals
        self.save_settings_btn.clicked.connect(self.save_settings)
        self.reset_settings_btn.clicked.connect(self.reset_settings_to_default)

        # Initialize
        self.configuration_page = EISWizardToolkitConfiguration()
        self.settings_tabs.addTab(self.configuration_page, "EIS Toolkit configuration")

        self.default_base_raster.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.raster_color_ramp_selection = QgsColorRampButton()
        self.color_ramp_layout.addWidget(self.raster_color_ramp_selection)
        self.load_settings()  # Initialize UI from settings

    def load_settings(self):
        """Load settings and set selections accordingly."""
        self.dock_wizard_selection.setChecked(EISSettingsManager.get_dock_wizard_selection())
        self.minimal_menu_selection.setChecked(EISSettingsManager.get_minimal_menu_selection())
        self.raster_color_ramp_selection.setColorRamp(EISSettingsManager.get_raster_color_ramp())
        self.default_color_selection.setColor(EISSettingsManager.get_default_color())
        self.categorical_palette_selection.setCurrentText(EISSettingsManager.get_default_categorical_palette())
        self.continuous_palette_selection.setCurrentText(EISSettingsManager.get_default_continuous_palette())
        self.layer_group_selection.setChecked(EISSettingsManager.get_layer_group_selection())
        self.default_base_raster.setLayer(EISSettingsManager.get_default_base_raster())


    def save_settings(self):
        """Save current selections."""
        EISSettingsManager.set_dock_wizard_selection(self.dock_wizard_selection.isChecked())
        EISSettingsManager.set_minimal_menu_selection(self.minimal_menu_selection.isChecked())
        EISSettingsManager.set_raster_color_ramp(self.raster_color_ramp_selection.colorRamp())
        EISSettingsManager.set_color_selection(self.default_color_selection.color())
        EISSettingsManager.set_categorical_palette_selection(self.categorical_palette_selection.currentText())
        EISSettingsManager.set_continuous_palette_selection(self.continuous_palette_selection.currentText())
        EISSettingsManager.set_layer_group_selection(self.layer_group_selection.isChecked())
        EISSettingsManager.set_default_base_raster(self.default_base_raster.currentLayer())
        
        self.minimal_menu_setting_changed.emit(self.minimal_menu_selection.isChecked())
        iface.messageBar().pushSuccess("Success: ", "Saved EIS QGIS plugin settings.")


    def reset_settings_to_default(self):
        """Set selections to defaults. Does not save."""
        defaults = EISSettingsManager.DEFAULTS

        self.dock_wizard_selection.setChecked(defaults[EISSettingsManager.DOCK_SETTING] == "true")
        self.minimal_menu_selection.setChecked(defaults[EISSettingsManager.MINIMAL_MENU_SETTING] == "true")
        self.raster_color_ramp_selection.setColorRamp(defaults[EISSettingsManager.RASTER_COLOR_RAMP_SETTING])
        self.default_color_selection.setColor(defaults[EISSettingsManager.COLOR_SETTING])
        self.categorical_palette_selection.setCurrentText(defaults[EISSettingsManager.CATEGORICAL_PALETTE_SETTING])
        self.continuous_palette_selection.setCurrentText(defaults[EISSettingsManager.CONTINUOUS_PALETTE_SETTING])
        self.layer_group_selection.setChecked(defaults[EISSettingsManager.LAYER_GROUP_SETTING] == "true")
        self.default_base_raster.setLayer(defaults[EISSettingsManager.DEFAULT_BASE_RASTER])

        iface.messageBar().pushInfo("Info: ", "EIS QGIS plugin settings reset.")
