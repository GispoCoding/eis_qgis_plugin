from qgis.core import QgsMapLayer
from qgis.gui import QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import QSizePolicy, QWidget


class EISExploratoryAnalysis(QWidget):
    """Template / parent class for exploratory analysis classes in EIS Wizard"""

    def __init__(self, parent) -> None:

        # DECLARE TYPES
        self.layer: QgsMapLayerComboBox
        
        # Initialize
        super().__init__(parent)
        self.setupUi(self)

        self.original_height = self.height()

    
    def update_layer(self, layer: QgsMapLayer):
        """Update widgets when layer is changed. Should be implemented in the child class."""
        raise NotImplementedError("Update layer needs to be defined in child class.")
    
    def reset(self):
        """Reset plot parameters to defaults."""
        raise NotImplementedError("Update layer needs to be defined in child class.")

    def resize_parameter_box(self, collapsed: bool):
        """Resize self and the parent widget (QStackedWidget) according to collapse signal."""
        if collapsed:
            self.setMinimumHeight(self.collapsed_height)
            self.setMaximumHeight(self.collapsed_height)
        else:
            self.setMinimumHeight(self.original_height)
            self.setMaximumHeight(self.original_height)
        container = self.parentWidget()
        container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        container.setMinimumHeight(self.height())