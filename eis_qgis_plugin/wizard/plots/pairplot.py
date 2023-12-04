import seaborn as sns
from qgis.gui import QgsColorButton, QgsMapLayerComboBox, QgsOpacityWidget
from qgis.PyQt.QtWidgets import QComboBox, QListWidget, QPushButton, QWidget

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QWidget = load_ui("wizard_plot_pairplot.ui")


class EISWizardPairplot(QWidget, FORM_CLASS):

    pairplot_layer: QgsMapLayerComboBox
    pairplot_fields: QListWidget

    pairplot_color: QgsColorButton
    pairplot_opacity: QgsOpacityWidget
    pairplot_log_scale: QComboBox
    pairplot_kind: QComboBox
    pairplot_diagonal_kind: QComboBox

    pairplot_select_all_btn: QPushButton
    pairplot_deselect_all_btn: QPushButton


    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)


    def plot(self, ax):
        penguins = sns.load_dataset("penguins")

        grid = sns.pairplot(
            data=penguins,
            # vars=["flipper_length_mm", "bill_length_mm"],
            hue="species",
            palette="dark",
        )

        return grid.figure


    def reset(self):
        pass
