from typing import List

from qgis.core import QgsApplication, QgsMapLayerProxyModel
from qgis.gui import QgsMapLayerComboBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QHeaderView, QLabel, QLineEdit, QPushButton, QSizePolicy, QTableWidget

HEADER_ROW_HEIGHT = 23

class ModelDataTable(QTableWidget):
    """
    Class for displaying model data (evidence layers/data) in testing/application phase.
    
    This table does not have "add" or "remove" buttons, but creates as many rows as the selected model
    used in training phase.
    """

    def __init__(self, parent, row_height: int = 26) -> None:
        super().__init__(parent)

        self.row_height = row_height

        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Tag", "Data"])
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setColumnWidth(0, 150)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        self.setMinimumHeight(23)
        self.setMaximumHeight(23)


    def load_model(self, tags: List[str]):
        """Load information about the selected model (number of rows/layers and corresponding tags)."""
        # Remove all previous rows
        self.setRowCount(0)

        # Set table size according to number of evidence layers / rows
        nr_of_rows = len(tags)
        self.setMinimumHeight(HEADER_ROW_HEIGHT + nr_of_rows * self.row_height)
        self.setMaximumHeight(HEADER_ROW_HEIGHT + nr_of_rows * self.row_height)

        for i, tag in enumerate(tags):
            self.insertRow(i)
            tag_label = QLabel()
            tag_label.setText(tag)
            self.setCellWidget(i, 0, tag_label)
            layer_selection = QgsMapLayerComboBox()
            layer_selection.setFilters(QgsMapLayerProxyModel.RasterLayer)
            self.setCellWidget(i, 1, layer_selection)

            self.setRowHeight(i, self.row_height)


class ModelTrainingDataTable(QTableWidget):
    """
    Class for displaying model data (evidence layers/data) in training phase.
    
    This table has "add" or "remove" buttons to control how many rows are used.
    """

    def __init__(self, parent, row_height: int = 26):
        super().__init__(parent)

        self.row_height = row_height

        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Tag", "Data", "Add", "Delete"])
        self.setColumnWidth(0, 150)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setColumnWidth(2, 50)
        self.setColumnWidth(3, 50)

        self.setMinimumHeight(23)

        self.add_row()


    def create_buttons(self):
        """Create "add" and "delete" buttons the table."""
        add_row_btn = QPushButton()
        add_row_btn.setIcon(QIcon(QgsApplication.iconPath('symbologyAdd.svg')))
        add_row_btn.setToolTip('Add a row below.')
        remove_row_btn = QPushButton()
        remove_row_btn.setIcon(QIcon(QgsApplication.iconPath('symbologyRemove.svg')))
        remove_row_btn.setToolTip('Remove row.')

        add_row_btn.clicked.connect(self.add_row)
        remove_row_btn.clicked.connect(self.remove_row)

        return add_row_btn, remove_row_btn


    def add_row(self):
        """Add a row in the table."""
        # Find row index
        rows = self.rowCount()
        if rows == -1:
            rows = 0

        selection = self.selectedIndexes()
        row_index = rows if len(selection) <= 0 else selection[0].row() + 1

        # Create row and set row and table size
        self.insertRow(row_index)
        self.setRowHeight(row_index, self.row_height)
        self.setMinimumHeight(self.minimumHeight() + self.row_height)

        # Add widgets to row
        add_btn, remove_btn = self.create_buttons()

        self.setCellWidget(row_index, 0, QLineEdit())
        layer_selection = QgsMapLayerComboBox()
        layer_selection.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.setCellWidget(row_index, 1, layer_selection)
        self.setCellWidget(row_index, 2, add_btn)
        self.setCellWidget(row_index, 3, remove_btn)

        # Reset selection
        self.clearSelection()


    def remove_row(self):
        """Remove selected row from the table."""
        rows = self.rowCount()
        if rows == 1:  # Can't remove the last row
            return
        selection = self.selectedIndexes()
        row_index = rows - 1 if len(selection) <= 0 else selection[0].row()
        
        # Remove row and set table size
        self.removeRow(row_index)
        self.setMinimumHeight(self.minimumHeight() - self.row_height)

        # Reset selection
        self.clearSelection()