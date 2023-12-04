from enum import Enum

from qgis.core import QgsColorRamp, QgsVectorLayer
from qgis.gui import QgsColorButton
from qgis.PyQt.QtGui import QColor

from eis_qgis_plugin import pyqtgraph as pg

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


def create_brush(color_selection: QgsColorButton, alpha: int):
    q_color = color_selection.color()
    red, green, blue = q_color.red(), q_color.green(), q_color.blue()
    return pg.mkBrush(color=(red, green, blue, alpha), width=3)


def create_pen(color_selection: QgsColorButton, alpha: int):
    q_color = color_selection.color()
    red, green, blue = q_color.red(), q_color.green(), q_color.blue()
    return pg.mkPen(color=(red, green, blue, alpha), width=3)


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
