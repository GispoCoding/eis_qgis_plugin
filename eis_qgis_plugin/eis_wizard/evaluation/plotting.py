import os

from qgis import processing
from qgis.core import QgsApplication, QgsMapLayerProxyModel
from qgis.gui import QgsFileWidget, QgsMapLayerComboBox, QgsSpinBox
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QPixmap
from qgis.PyQt.QtWidgets import QComboBox, QDialogButtonBox, QGroupBox, QLabel, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.message_manager import EISMessageManager
from eis_qgis_plugin.utils.misc_utils import get_output_path, set_file_widget_placeholder_text, set_filter

FORM_CLASS: QWidget = load_ui("evaluation/evaluation_plotting.ui")



class EISWizardEvaluationPlotting(QWidget, FORM_CLASS):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # DECLARE TYPES
        self.plot_type_selection: QComboBox
        self.plot_parametrs_box: QGroupBox
        self.deposits: QgsMapLayerComboBox
        self.predictions_label: QLabel
        self.predictions: QgsMapLayerComboBox
        self.probabilities_label: QLabel
        self.probabilities: QgsMapLayerComboBox
        self.number_of_bins_label: QLabel
        self.number_of_bins: QgsSpinBox
        self.save_dpi: QgsSpinBox
        self.output_file: QgsFileWidget

        self.plot_label: QLabel

        self.button_box: QDialogButtonBox

        # INIT
        self.clear_plot_btn = self.button_box.addButton("Clear plot", QDialogButtonBox.ActionRole)
        self.clear_plot_btn.setIcon(QIcon(QgsApplication.getThemeIcon("mActionDeleteSelected.svg")))
        self.clear_plot_btn.clicked.connect(self.clear_plot)
        self.create_plot_btn = self.button_box.addButton("Create plot", QDialogButtonBox.ActionRole)
        self.create_plot_btn.setIcon(QIcon(QgsApplication.getThemeIcon("mActionStart.svg")))
        self.create_plot_btn.clicked.connect(self.create_plot)
        self.create_plot_btn.setDefault(True)

        self.plot_type_selection.currentTextChanged.connect(self.update_parameters)
        self.update_parameters(self.plot_type_selection.currentText())

        self.deposits.setFilters(QgsMapLayerProxyModel.RasterLayer)
        set_filter(self.output_file, "image")
        set_file_widget_placeholder_text(self.output_file)


    def update_parameters(self, plot_type_name: str):
        if plot_type_name.lower() == "calibration curve":
            self.number_of_bins.show()
            self.number_of_bins_label.show()
        else:
            self.number_of_bins.hide()
            self.number_of_bins_label.hide()

        if plot_type_name.lower() == "confusion matrix":
            self.predictions_label.setEnabled(True)
            self.predictions.setEnabled(True)

            self.probabilities_label.setEnabled(False)
            self.probabilities.setEnabled(False)
        else:
            self.predictions_label.setEnabled(False)
            self.predictions.setEnabled(False)

            self.probabilities_label.setEnabled(True)
            self.probabilities.setEnabled(True)


    def create_plot(self):
        plot_type = self.plot_type_selection.currentText().lower()
        params = {
            "true_labels": self.deposits.currentLayer(),
            "show_plot": False,
            "save_dpi": self.save_dpi.value() if self.save_dpi.value() > 0 else None,
            "output_file": get_output_path(self.output_file)
        }
        if plot_type == "confusion matrix":
            alg_name = "eis:plot_confusion_matrix"
            params["predictions"] = self.predictions.currentLayer()
        elif plot_type == "calibration curve":
            alg_name = "eis:plot_calibration_curve"
            params["n_bins"] = self.number_of_bins.value()
            params["probabilities"] = self.probabilities.currentLayer()
        elif plot_type == "det curve":
            alg_name = "eis:plot_det_curve"
            params["probabilities"] = self.probabilities.currentLayer()
        elif plot_type == "precision-recall curve":
            alg_name = "eis:plot_precision_recall_curve"
            params["probabilities"] = self.probabilities.currentLayer()
        elif plot_type == "roc curve":
            alg_name = "eis:plot_roc_curve"
            params["probabilities"] = self.probabilities.currentLayer()
        else:
            pass

        result = processing.run(alg_name, params)
        plot_fp = result["output_file"]
        # self.plot_label.setScaledContents(True)
        if os.path.exists(plot_fp):
            pixmap = QPixmap(plot_fp)
            scaled_pixmap = pixmap.scaled(
                self.plot_label.size(), 
                aspectRatioMode=Qt.KeepAspectRatio,
                transformMode=Qt.SmoothTransformation
            )
            self.plot_label.setPixmap(scaled_pixmap)
        else:
            EISMessageManager().show_message("Failed to produce plot, check log messages for error details.", "error")

    def clear_plot(self):
        self.plot_label.clear()
