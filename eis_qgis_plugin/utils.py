import os

from qgis.core import QgsProject
from qgis.gui import QgsFileWidget
from qgis.PyQt.QtWidgets import QLayout, QLineEdit

PLUGIN_PATH = os.path.dirname(__file__)

TEMPORARY_OUTPUT = 'TEMPORARY_OUTPUT'


def set_file_widget_placeholder_text(
    file_widget: QgsFileWidget, placeholder_text = "[Save to temporary file]"
) -> bool:
    """Tries to find QLineEdit in a QgsFileWidget and set its placeholder text."""
    line_edit = file_widget.findChild(QLineEdit)
    if line_edit:
        line_edit.setPlaceholderText(placeholder_text)
        return True
    return False


def clear_layout(layout: QLayout):
    for i in reversed(range(layout.count())):
        widget = layout.itemAt(i).widget()
        if widget is not None:
            widget.deleteLater()


def add_output_layer_to_group(layer, group_name: str, subgroup_name: str):
    QgsProject.instance().addMapLayer(layer, False)
    root = QgsProject.instance().layerTreeRoot()
    group = root.findGroup(group_name)
    if not group:
        group = root.addGroup(group_name)
    
    category_subgroup = group.findGroup(subgroup_name)
    if not category_subgroup:
        category_subgroup = group.addGroup(subgroup_name)
    
    category_subgroup.addLayer(layer)
