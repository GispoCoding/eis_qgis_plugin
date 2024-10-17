from qgis.core import QgsMapLayer
from qgis.PyQt.QtWidgets import QWidget


class EISExploratoryAnalysis(QWidget):
    """Template / parent class for exploratory analysis classes in EIS Wizard"""

    def __init__(self, parent) -> None:

        # Initialize
        super().__init__(parent)
        self.setupUi(self)

    
    def update_layer(self, layer: QgsMapLayer):
        """Update widgets when layer is changed. Should be implemented in the child class."""
        raise NotImplementedError("Update layer needs to be defined in child class.")
    
    def reset(self):
        """Reset plot parameters to defaults."""
        raise NotImplementedError("Reset needs to be defined in child class.")
