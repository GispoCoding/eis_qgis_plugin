from qgis.PyQt.QtWidgets import QComboBox

import eis_qgis_plugin.libs.seaborn as sns
from eis_qgis_plugin.eis_wizard.eda.plots.plot_template import EISPlot


class EISWizardPairplot(EISPlot):
    """
    Parent class for EIS-Seaborn pairplots.
    """
    def __init__(self, parent=None) -> None:
        
        # DECLARE TYPES
        self.kind: QComboBox
        self.diagonal_kind: QComboBox

        # Initialize
        super().__init__(parent)


    def plot_example(self, ax):
        """Produce example plot using SNS data."""
        penguins = sns.load_dataset("penguins")

        grid = sns.pairplot(
            data=penguins,
            hue="species",
            palette="dark",
        )

        return grid.figure
    

    def reset(self):
        """Reset parameters to defaults."""
        super().reset()

        self.kind.setCurrentIndex(0)
        self.diagonal_kind.setCurrentIndex(0)