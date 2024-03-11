from qgis.gui import QgsFileWidget
from qgis.PyQt.QtWidgets import QLineEdit

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
