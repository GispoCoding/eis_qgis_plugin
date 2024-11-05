from typing import Dict, List, Tuple

from qgis.core import QgsApplication, QgsMapLayerProxyModel, QgsRasterLayer
from qgis.gui import QgsMapLayerComboBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QHeaderView, QLabel, QLineEdit, QPushButton, QSizePolicy, QTableWidget

from eis_qgis_plugin.utils.message_manager import EISMessageManager


class ModelDataTable(QTableWidget):
    """
    Class for displaying model data (evidence layers/data) in testing/application phase.
    
    This table does not have "add" or "remove" buttons, but creates as many rows as the selected model
    used in training phase.
    """

    HEADER_ROW_HEIGHT = 23


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
        self.setMinimumHeight(self.HEADER_ROW_HEIGHT + nr_of_rows * self.row_height)
        self.setMaximumHeight(self.HEADER_ROW_HEIGHT + nr_of_rows * self.row_height)

        for i, tag in enumerate(tags):
            self.insertRow(i)
            tag_label = QLabel()
            tag_label.setText(tag)
            self.setCellWidget(i, 0, tag_label)
            layer_selection = QgsMapLayerComboBox()
            layer_selection.setFilters(QgsMapLayerProxyModel.RasterLayer)
            self.setCellWidget(i, 1, layer_selection)

            self.setRowHeight(i, self.row_height)


    def get_tags(self) -> List[str]:
        [self.cellWidget(row, 0).currentLayer() for row in range(self.rowCount())]


    def get_layers(self) -> List[QgsRasterLayer]:
        return [self.cellWidget(row, 1).currentLayer() for row in range(self.rowCount())]


class ModelHistoryTable(QTableWidget):
    """
    Class for displaying model data in history page.
    
    This table does not have "add" or "remove" buttons, but creates as many rows as the selected model
    used in training phase.
    """

    HEADER_ROW_HEIGHT = 23


    def __init__(self, parent, row_height: int = 26) -> None:
        super().__init__(parent)

        self.row_height = row_height

        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Tag", "Layer name", "Layer filepath"])
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setColumnWidth(0, 150)
        # self.setColumnWidth(1, 200)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.setMinimumHeight(23)
        self.setMaximumHeight(23)


    def reset_table(self):
        self.setRowCount(0)
        self.setMinimumHeight(23)
        self.setMaximumHeight(23)


    def load_model(self, tags: List[str], evidence_data: List[Tuple[str, str]]):
        """Load information about the selected model (number of rows/layers and corresponding tags)."""
        if len(tags) != len(evidence_data):
            EISMessageManager().show_message(
                "Number of evidence datasets should match the number of given tags!", "invalid"
            )
            return

        # Remove all previous rows
        self.setRowCount(0)

        # Set table size according to number of evidence layers / rows
        nr_of_rows = len(tags)
        self.setMinimumHeight(self.HEADER_ROW_HEIGHT + nr_of_rows * self.row_height)
        self.setMaximumHeight(self.HEADER_ROW_HEIGHT + nr_of_rows * self.row_height)

        for i, tag in enumerate(tags):
            self.insertRow(i)

            # Tag
            tag_label = QLabel()
            tag_label.setText(tag)
            self.setCellWidget(i, 0, tag_label)

            # Name
            name_label = QLabel()
            name_label.setText(evidence_data[i][0])
            self.setCellWidget(i, 1, name_label)

            # Filepath
            filepath_label = QLabel()
            filepath_label.setText(evidence_data[i][1])
            self.setCellWidget(i, 2, filepath_label)

            self.setRowHeight(i, self.row_height)


class ModelTrainingDataTable(QTableWidget):
    """
    Class for displaying model data (evidence layers/data) in training phase.
    
    This table has "add" or "remove" buttons to control how many rows are used.
    """

    def __init__(
        self,
        parent,
        add_tag_column: bool = True,
        inital_rows: int = 1,
        row_height: int = 26,
        min_rows: int = 1
    ):
        super().__init__(parent)

        self.row_height = row_height
        self.tag_column = add_tag_column
        self.min_rows = min_rows

        if add_tag_column:
            self.init_with_tag()
        else:
            self.init_without_tag()

        self.setMinimumHeight(23)

        for _ in range(inital_rows):
            self.add_row()


    def init_with_tag(self):
        self.labels = ["Tag", "Data", "Add", "Delete"]
        self.setColumnCount(len(self.labels))
        self.setHorizontalHeaderLabels(self.labels)
        self.setColumnWidth(0, 150)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setColumnWidth(2, 50)
        self.setColumnWidth(3, 50)


    def init_without_tag(self):
        self.labels = ["Data", "Add", "Delete"]
        self.setColumnCount(len(self.labels))
        self.setHorizontalHeaderLabels(self.labels)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.setColumnWidth(1, 50)
        self.setColumnWidth(2, 50)


    def get_tags(self) -> List[str]:
        if not self.tag_column:
            raise NotImplementedError("The model data table was initialized without tag column.")
        return [self.cellWidget(row, 0).text() for row in range(self.rowCount())]


    def get_layers(self) -> List[QgsRasterLayer]:
        layer_col = 1 if self.tag_column else 0
        return [self.cellWidget(row, layer_col).currentLayer() for row in range(self.rowCount())]
    

    def get_tagged_layers(self) -> Dict[str, QgsRasterLayer]:
        if not self.tag_column:
            raise NotImplementedError("The model data table was initialized without tag column.")
        return {
            self.cellWidget(row, 0).text(): self.cellWidget(row, 1).currentLayer()
            for row in range(self.rowCount())
        }
    

    def generate_tags(self):
        if not self.tag_column:
            raise NotImplementedError("The model data table was initialized without tag column.")
        for row in range(self.rowCount()):
            layer_name = self.cellWidget(row, 1).currentLayer().name()
            self.cellWidget(row, 0).setText(layer_name)


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

        # Add widgets
        if self.tag_column:
            self.add_row_widgets_tag(row_index)
        else:
            self.add_row_widgets_without_tag(row_index)

        # Reset selection
        self.clearSelection()


    def add_row_widgets_tag(self, row_index: int):
        add_btn, remove_btn = self.create_buttons()

        self.setCellWidget(row_index, 0, QLineEdit())
        layer_selection = QgsMapLayerComboBox()
        layer_selection.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.setCellWidget(row_index, 1, layer_selection)
        self.setCellWidget(row_index, 2, add_btn)
        self.setCellWidget(row_index, 3, remove_btn)


    def add_row_widgets_without_tag(self, row_index: int):
        add_btn, remove_btn = self.create_buttons()

        layer_selection = QgsMapLayerComboBox()
        layer_selection.setFilters(QgsMapLayerProxyModel.RasterLayer)
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

        # Reset selection
        self.clearSelection()
