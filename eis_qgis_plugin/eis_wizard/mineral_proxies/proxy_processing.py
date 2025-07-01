from typing import Any, Dict, Literal

from qgis.core import QgsApplication, QgsMapLayerProxyModel, QgsProject, QgsRasterLayer
from qgis.gui import QgsDoubleSpinBox, QgsExtentGroupBox, QgsFileWidget, QgsMapLayerComboBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialogButtonBox,
    QLabel,
    QLayout,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QWidget,
)

from eis_qgis_plugin.utils.algorithm_execution import AlgorithmExecutor
from eis_qgis_plugin.utils.message_manager import EISMessageManager
from eis_qgis_plugin.utils.misc_utils import (
    add_output_layer_to_group,
    # apply_color_ramp_to_raster_layer,
    get_output_layer_name,
    set_file_widget_placeholder_text,
    set_filter,
)
from eis_qgis_plugin.utils.model_feedback import EISProcessingFeedback
from eis_qgis_plugin.utils.settings_manager import EISSettingsManager


class EISWizardProxyProcess(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.proxy_name_label: QLabel
        self.process_step_label: QLabel

        self.log: QTextEdit
        self.progress_bar: QProgressBar
        self.executor: AlgorithmExecutor
        self.mineral_system_component: str
        self.mineral_system: str

        self.output_raster_path: QgsFileWidget
        self.output_raster_settings: QComboBox
        self.output_raster_settings_pages: QStackedWidget
        self.base_raster: QgsMapLayerComboBox
        self.pixel_size: QgsDoubleSpinBox
        self.extent: QgsExtentGroupBox

        self.navigation_btn_layout: QLayout
        # self.run_btn: QPushButton
        # self.cancel_btn: QPushButton
        self.button_box: QDialogButtonBox
        self.back_btn: QPushButton
        self.finish_btn: QPushButton
        self.next_btn: QPushButton


    def initialize(self, process_type: Literal["single_step", "multi_step", "multi_step_final"]):
        # Set file filter and placeholder text for output raster
        set_filter(self.output_raster_path, "raster")
        set_file_widget_placeholder_text(self.output_raster_path)

        # Connect output raster settings signal
        self.output_raster_settings.currentIndexChanged.connect(self.on_output_raster_settings_changed)

        # Set name label
        self.proxy_name_label.setText(self.proxy_name_label.text() + self.proxy_name)

        # Set base raster
        self.base_raster.setFilters(QgsMapLayerProxyModel.RasterLayer)
        default_base_raster = EISSettingsManager.get_default_base_raster()
        if default_base_raster is not None:
            self.base_raster.setLayer(default_base_raster)

        # Create feedback
        self.feedback = EISProcessingFeedback(text_edit=self.log, progress_bar=self.progress_bar)

        # Create executor and connect signals
        self.executor = AlgorithmExecutor()
        self.executor.finished.connect(self.on_algorithm_executor_finished)
        self.executor.terminated.connect(self.on_algorithm_executor_terminated)
        self.executor.error.connect(self.on_algorithm_executor_error)

        # Connect and initialize execution buttons
        self.cancel_btn = self.button_box.button(QDialogButtonBox.Cancel)
        self.cancel_btn.setText("Cancel")
        self.run_btn = self.button_box.button(QDialogButtonBox.Ok)
        self.run_btn.setText("Run")
        self.run_btn.setIcon(QIcon(QgsApplication.getThemeIcon("mActionStart.svg")))

        self.run_btn.clicked.connect(self.run)
        self.cancel_btn.clicked.connect(lambda: self.executor.cancel() if self.executor is not None else None)
        self.back_btn.clicked.connect(
            lambda: self.proxy_manager.proxy_pages.setCurrentIndex(self.proxy_manager.proxy_pages.currentIndex() - 1)
                if not self.check_if_executor_running()
                else None
            )
        self.next_btn.clicked.connect(
            lambda: self.proxy_manager.proxy_pages.setCurrentIndex(self.proxy_manager.proxy_pages.currentIndex() + 1)
            if not self.check_if_executor_running()
            else None
        )
        self.finish_btn.clicked.connect(
            lambda: self.proxy_manager.proxy_pages.setCurrentIndex(0)
            if not self.check_if_executor_running()
            else None
        )

        # Configure page navigation buttons and name label based on process type
        if process_type == "single_step":
            self.next_btn.setEnabled(False)
            self.process_step_label.setEnabled(False)
            self.default_output_name = self.proxy_name
        elif process_type == "multi_step":
            self.finish_btn.setEnabled(False)
            self.process_step_label.setText(self.process_step_label.text() + "1/2")  # NOTE: 2 steps assumed for now
            self.default_output_name = self.WORKFLOW_NAME + " result ― " + self.proxy_name
        elif process_type == "multi_step_final":
            self.next_btn.setEnabled(False)
            self.process_step_label.setText(self.process_step_label.text() + "2/2")
            self.default_output_name = self.proxy_name
        else:
            raise TypeError(f"Unrecognized proxy workflow process type: {process_type}")


    def on_algorithm_executor_finished(self, result, _):
        if self.feedback.no_errors:
            output_layer = QgsRasterLayer(
                result["output_raster"], get_output_layer_name(self.output_raster_path, self.default_output_name)
            )
            if EISSettingsManager.get_layer_group_selection():
                add_output_layer_to_group(
                    output_layer,
                    f"Mineral system proxies — {self.mineral_system}",
                    self.mineral_system_component.capitalize()
                )
            else:
                QgsProject.instance().addMapLayer(output_layer, True)

            if self.process_type == "multi_step":
                i = self.proxy_manager.proxy_pages.currentIndex() + 1
                self.proxy_manager.proxy_pages.widget(i).raster_layer.setLayer(output_layer)

            # apply_color_ramp_to_raster_layer(output_layer, EISSettingsManager.get_raster_color_ramp())


    def on_algorithm_executor_terminated(self):
        self.feedback = EISProcessingFeedback(text_edit=self.log, progress_bar=self.progress_bar)


    def on_algorithm_executor_error(self, error_message: str):
        pass


    def on_output_raster_settings_changed(self):
        raise NotImplementedError("'on_output_raster_settings_changed' needs to be implemented in child class!")


    def get_extent(self):
        current_extent = self.extent.outputExtent()
        if current_extent.isEmpty():
            return None
        return "{},{},{},{}".format(
            current_extent.xMinimum(),
            current_extent.xMaximum(),
            current_extent.yMinimum(),
            current_extent.yMaximum()
        )


    def get_output_raster_params(self) -> Dict[str, Any]:
        if self.output_raster_settings.currentIndex() == 0:
            base_raster = self.base_raster.currentLayer()
            if base_raster is None:
                EISMessageManager().show_message("Base raster is not defined", "invalid")
                return None
            params = {
                "base_raster": base_raster,
                "pixel_size": None,
                "extent": None
            }
        else:
            pixel_size = self.pixel_size.value()
            extent = self.get_extent()
            if pixel_size <= 0 or extent is None:
                EISMessageManager().show_message("Pixel value and/or extent are not defined", "invalid")
                return None
            params = {
                "base_raster": None,
                "pixel_size": pixel_size,
                "extent": extent
            }
        return params


    def check_if_executor_running(self) -> bool:
        if self.executor.is_running:
            EISMessageManager().show_message("Cannot leave page when computation is running!", "error")
            return True
        return False
