from typing import Optional

from qgis.core import (
    QgsApplication,
    QgsFieldProxyModel,
    QgsMapLayer,
    QgsMapLayerProxyModel,
    QgsRasterLayer,
    QgsVectorLayer,
)
from qgis.gui import QgsFieldComboBox, QgsMapLayerComboBox, QgsRasterBandComboBox
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QComboBox, QHeaderView, QPushButton, QTableWidget


class LayerDataTable(QTableWidget):
    """
    Class for displaying vector and raster layers.
    
    This table has "add" or "remove" buttons to control how many rows are used.
    """

    size_changed = pyqtSignal(int)

    def __init__(
        self,
        parent,
        initial_rows: int = 1,
        row_height: int = 26,
        min_rows: int = 1,
        dtype: Optional[QgsMapLayer] = None,
        field_selection: bool = False,
    ):
        super().__init__(parent)

        self.row_height = row_height
        self.min_rows = min_rows
        self.initial_rows = initial_rows
        self.dtype = dtype
        self.field_selection = field_selection
        
        if self.field_selection:
            self.labels = ["Layer", "Selection", "Add", "Delete"]
        else:
            self.labels = ["Layer", "Add", "Delete"]

        self.setColumnCount(len(self.labels))
        self.setHorizontalHeaderLabels(self.labels)
        self.setColumnWidth(0, 150)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        if self.field_selection:
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        self.setColumnWidth(1, 50)
        self.setColumnWidth(2, 50)

        self.setMinimumHeight(23)
        

    def create_buttons(self):
        """Create "add" and "delete" buttons on the table."""
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
        self.size_changed.emit(self.row_height)

        # Add widgets
        self.add_row_widgets(row_index)

        # Reset selection
        self.clearSelection()


    def add_row_widgets(self, row_index):
        add_btn, remove_btn = self.create_buttons()

        layer_selection = QgsMapLayerComboBox()
        if self.dtype == QgsRasterLayer:
            layer_selection.setFilters(QgsMapLayerProxyModel.RasterLayer)

        elif self.dtype == QgsVectorLayer:
            layer_selection.setFilters(QgsMapLayerProxyModel.VectorLayer)

        selection = QComboBox()
        field_selection = QgsFieldComboBox()
        field_selection.setFilters(QgsFieldProxyModel.Filter.Numeric)
        band_selection = QgsRasterBandComboBox()

        if self.field_selection:
            self.setCellWidget(row_index, 0, layer_selection)
            self.setCellWidget(row_index, 1, selection)
            self.setCellWidget(row_index, 2, add_btn)
            self.setCellWidget(row_index, 3, remove_btn)
            
            layer_selection.layerChanged.connect(
                lambda new_layer: (
                    field_selection.setLayer(new_layer) if new_layer.type() == QgsMapLayer.VectorLayer else
                    band_selection.setLayer(new_layer),
                    self.setCellWidget(row_index, 1, 
                        field_selection if new_layer.type() == QgsMapLayer.VectorLayer else
                        band_selection
                    )
                )
            )
        else:
            self.setCellWidget(row_index, 0, layer_selection)
            self.setCellWidget(row_index, 1, add_btn)
            self.setCellWidget(row_index, 2, remove_btn)


    def remove_row(self):
        """Remove selected row from the table."""
        rows = self.rowCount()
        if rows == self.min_rows:  # Can't remove the last row
            return
        selection = self.selectedIndexes()
        row_index = rows - 1 if len(selection) <= 0 else selection[0].row()
        
        # Remove row and set table size
        self.removeRow(row_index)
        self.setMinimumHeight(self.minimumHeight() - self.row_height)
        self.size_changed.emit(-self.row_height)

        # Reset selection
        self.clearSelection()