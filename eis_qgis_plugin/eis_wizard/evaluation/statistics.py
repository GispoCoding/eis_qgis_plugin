from qgis import processing
from qgis.core import QgsApplication, QgsMapLayerProxyModel
from qgis.gui import QgsMapLayerComboBox, QgsSpinBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QDialog,
    QLineEdit,
    QPushButton,
    QWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui
from eis_qgis_plugin.utils.message_manager import EISMessageManager

FORM_CLASS: QDialog = load_ui("evaluation/evaluation_statistics.ui")


class EISWizardEvaluationStatistics(QWidget, FORM_CLASS): 

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # DECLARE TYPES
        self.deposits_layer: QgsMapLayerComboBox
        self.predicted_labels_layer: QgsMapLayerComboBox
        self.predicted_probabilities_layer: QgsMapLayerComboBox

        self.decimals: QgsSpinBox
        self.compute_btn: QPushButton

        self.accuracy: QLineEdit
        self.precision: QLineEdit
        self.recall: QLineEdit
        self.f1: QLineEdit

        self.true_positives: QLineEdit
        self.false_negatives: QLineEdit
        self.false_positives: QLineEdit
        self.true_negatives: QLineEdit

        self.roc_auc: QLineEdit
        self.log_loss: QLineEdit
        self.average_precision: QLineEdit
        self.brier_score_loss: QLineEdit

        # INITIALIZE
        self.deposits_layer.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.predicted_labels_layer.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.predicted_labels_layer.setLayer(None)
        self.predicted_probabilities_layer.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.predicted_probabilities_layer.setLayer(None)

        self.compute_btn.setIcon(QIcon(QgsApplication.getThemeIcon("mActionStart.svg")))
        self.compute_btn.setDefault(True)
        self.compute_btn.clicked.connect(self.compute_metrics)

        # Map widgets to the processing algorithm return dictionary keys
        self.label_stats_widgets = {
            "Accuracy": self.accuracy,
            "Precision": self.precision,
            "Recall": self.recall,
            "F1_score": self.f1,
            "True_negatives": self.true_negatives,
            "False_negatives": self.false_negatives,
            "False_positives": self.false_positives,
            "True_positives": self.true_positives
        }
        self.probability_stats_widgets = {
            "roc_auc": self.roc_auc,
            "log_loss": self.log_loss,
            "average_precision": self.average_precision,
            "brier_score_loss": self.brier_score_loss
        }


    def compute_metrics(self):
        if self.predicted_labels_layer.currentLayer() is None \
            and self.predicted_probabilities_layer.currentLayer() is None:
            EISMessageManager().show_message(
                "Select predicted classification/label raster, predicted probabilities \
                    raster or both to compute metrics.",
                "invalid"
            )
            return
        if self.predicted_labels_layer.currentLayer() is not None:
            self._compute_label_metrics()

        if self.predicted_probabilities_layer.currentLayer() is not None:
            self._compute_probability_metrics()


    def _compute_label_metrics(self):
        results = processing.run(
            "eis:summarize_label_metrics_binary",
            {
                "true_labels": self.deposits_layer.currentLayer(),
                "predictions": self.predicted_labels_layer.currentLayer(),
            },
        )
        if results == {}:
            EISMessageManager().show_message(
                "Failed to produce classification/label metrics, check log messages for error details.",
                "error"
            )
            return
        self._update_widgets(results, self.label_stats_widgets)


    def _compute_probability_metrics(self):
        results = processing.run(
            "eis:summarize_probability_metrics",
            {
                "true_labels": self.deposits_layer.currentLayer(),
                "probabilities": self.predicted_probabilities_layer.currentLayer(),
            },
        )
        if results == {}:
            EISMessageManager().show_message(
                "Failed to produce probability metrics, check log messages for error details.",
                "error"
            )
        self._update_widgets(results, self.probability_stats_widgets)


    def _update_widgets(self, results: dict, widget_map: dict):
        decimals = self.decimals.value()
        for dict_key, widget in widget_map.items():
            value = results.get(dict_key)
            if str(value) == "0.0":
                str_value = "0.0"
            elif str(value) == "0":
                str_value = "0"
            elif value:
                if decimals > 0:
                    str_value = str(round(value, decimals))
                else:
                    str_value = str(int(round(value, decimals)))
            else:
                str_value = ""
            widget.setText(str_value)
