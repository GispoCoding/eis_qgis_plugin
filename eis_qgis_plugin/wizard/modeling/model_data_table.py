from typing import Callable, Optional

from qgis.core import QgsApplication
from qgis.gui import QgsMapLayerComboBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QHeaderView, QPushButton, QSizePolicy, QTableWidget

# WIP

class ModelDataTable(QTableWidget):
        
    def __init__(self, parent, resize_callback: Optional[Callable] = None) -> None:
        super().__init__(parent)

        self.resize_callback = resize_callback

        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Data", "Add", "Delete"])
        self.setMinimumHeight(75)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Initialize table for training data
        self.setColumnWidth(0, 200)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.setColumnWidth(1, 50)
        self.setColumnWidth(2, 50)

        self.add_row_to_table()



    def create_table_buttons(self):
        """Create buttons for a row in the training data table widget."""
        add_row = QPushButton()
        add_row.setIcon(QIcon(QgsApplication.iconPath('symbologyAdd.svg')))
        add_row.setToolTip('Add a row below.')
        remove_row = QPushButton()
        remove_row.setIcon(QIcon(QgsApplication.iconPath('symbologyRemove.svg')))
        remove_row.setToolTip('Remove row.')

        add_row.clicked.connect(self.add_row_to_table)
        remove_row.clicked.connect(self.remove_row)

        return add_row, remove_row
    
    def remove_row(self):
        """Remove the selected row from the training data table widget."""
        rows = self.rowCount()
        if rows == 1:
            return
        selection = self.selectedIndexes()

        self.clearSelection()
        self.removeRow(rows - 1 if len(selection) <= 0 else selection[0].row())

        if self.resize_callback is not None:
            self.resize_callback(-25)
            # self.resize_container(-25)


    def get_training_layers(self):
        """Get all layers currently selected in the training data table."""
        return [self.cellWidget(row, 0).currentLayer() for row in range(self.rowCount())]


    def add_row_to_table(self):
        """Add a row in the training data table widget."""
        rows = self.rowCount()
        if rows == -1:
            rows = 0

        selection = self.selectedIndexes()
        row_index = rows if len(selection) <= 0 else selection[0].row() + 1

        self.insertRow(row_index)

        layer_widget = QgsMapLayerComboBox()

        add_btn, remove_btn = self.create_table_buttons()

        self.setCellWidget(row_index, 0, layer_widget)
        self.setCellWidget(row_index, 1, add_btn)
        self.setCellWidget(row_index, 2, remove_btn)

        self.clearSelection()

        if self.resize_callback is not None:
            self.resize_callback(25)
            # self.resize_container(25)