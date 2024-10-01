from enum import Enum
from typing import List

from qgis.core import QgsApplication, QgsColorRamp, QgsMapLayerProxyModel, QgsRasterLayer, QgsVectorLayer
from qgis.gui import QgsColorButton, QgsMapLayerComboBox
from qgis.PyQt.QtGui import QColor, QIcon
from qgis.PyQt.QtWidgets import QHeaderView, QPushButton, QTableWidget

# River nights in specific order, max 6 colors
DEFAULT_COLORS_CATECORIGAL = [
    (179, 0, 0),
    (68, 33, 175),
    (90, 212, 90),
    (235, 220, 120),
    (124, 17, 88),
    (0, 183, 199),
]

ALPHA = 150


class ChartType(Enum):
    LINE = 1
    SCATTER = 2
    BAR = 3
    BOX = 4
    HISTOGRAM = 5
    PARALLEL = 6


CHART_MAPPINGS = {
    "line plot": ChartType.LINE,
    "scatter plot": ChartType.SCATTER,
    "bar plot": ChartType.BAR,
    "box plot": ChartType.BOX,
    "histogram": ChartType.HISTOGRAM,
    "parallel coordinates": ChartType.PARALLEL,
}

# brushes = [
#     pg.mkBrush(color=(25, 132, 197, 150), width=3),
#     pg.mkBrush(color=(208, 238, 17, 150), width=3),
# ]


def update_color_selection(color_selection: QgsColorButton, plot_number: int) -> None:
    color = QColor(*DEFAULT_COLORS_CATECORIGAL[plot_number])
    color_selection.setColor(color)


# def create_brush(color_selection: QgsColorButton, alpha: int):
#     q_color = color_selection.color()
#     red, green, blue = q_color.red(), q_color.green(), q_color.blue()
#     return pg.mkBrush(color=(red, green, blue, alpha), width=3)


# def create_pen(color_selection: QgsColorButton, alpha: int):
#     q_color = color_selection.color()
#     red, green, blue = q_color.red(), q_color.green(), q_color.blue()
#     return pg.mkPen(color=(red, green, blue, alpha), width=3)


# def qgis_color_ramp_to_pyqtgraph(color_ramp: QgsColorRamp, n_colors=256):
#     color_array = []
#     for i in range(n_colors):
#         color = color_ramp.color(i / (n_colors - 1))
#         color_array.append([color.red(), color.green(), color.blue(), color.alpha()])
#     positions = np.linspace(0, 1, n_colors)
#     color_map = ColorMap(positions, color_array)
#     return color_map


def is_field_discrete(layer: QgsVectorLayer, field_name: str):
    """
    Check if the field is discrete or continuous based on its unique values.
    If the number of unique values is small compared to the total count, we consider it discrete.
    """
    unique_values = layer.uniqueValues(layer.fields().indexOf(field_name))
    total_count = layer.featureCount()

    # If less than 10% of the total count are unique, consider it discrete
    return len(unique_values) / total_count < 0.1


def generate_color_mapping(
    layer: QgsVectorLayer, field_name: str, color_ramp: QgsColorRamp
):
    """
    Generate a color mapping for a field using a color ramp.
    """
    unique_values = list(layer.uniqueValues(layer.fields().indexOf(field_name)))
    num_values = len(unique_values)

    color_mapping = {}
    for i, value in enumerate(unique_values):
        color = color_ramp.color(i / (num_values - 1) if num_values > 1 else 0.5)
        color_mapping[value] = color

    return color_mapping


def opacity_to_alpha(opacity: float):
    return opacity * 256


class RasterTable(QTableWidget):
    """
    Class for displaying rasters.

    This table has "add" or "remove" buttons to control how many rows are used.
    """

    def __init__(
        self,
        parent,
        inital_rows: int = 1,
        row_height: int = 26,
        min_rows: int = 1
    ):
        super().__init__(parent)

        self.row_height = row_height
        self.min_rows = min_rows
        self.labels = ["Data", "Add", "Delete"]
        self.setColumnCount(len(self.labels))
        self.setHorizontalHeaderLabels(self.labels)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.setColumnWidth(1, 50)
        self.setColumnWidth(2, 50)

        self.setMinimumHeight(23)

        for _ in range(inital_rows):
            self.add_row()

    
    def get_layers(self) -> List[QgsRasterLayer]:
        layer_col = 0
        return [self.cellWidget(row, layer_col).currentLayer() for row in range(self.rowCount())]
    

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

        # Add widgets
        self.add_row_widgets(row_index)

        # Reset selection
        self.clearSelection()


    def add_row_widgets(self, row_index: int):
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