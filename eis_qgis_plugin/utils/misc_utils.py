import os
import re
from enum import Enum
from typing import Any, Dict, Literal, Optional

from qgis.core import (
    QgsColorRamp,
    QgsColorRampShader,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingParameterDefinition,
    QgsProject,
    QgsRasterLayer,
    QgsRasterShader,
    QgsSingleBandPseudoColorRenderer,
)
from qgis.gui import QgsFileWidget
from qgis.PyQt.QtWidgets import QLayout, QLineEdit

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm
from eis_qgis_plugin.eis_processing.eis_toolkit_invoker import EISToolkitInvoker

TEMPORARY_OUTPUT = 'TEMPORARY_OUTPUT'
CLASSIFIER_METRICS = ["Accuracy", "Precision", "Recall", "F1"]
REGRESSOR_METRICS = ["MSE", "RMSE", "MAE", "R2"]
PLUGIN_PATH = os.path.dirname(os.path.dirname(__file__))
FILE_FILTERS = {
    "raster": "GeoTiff files (*.tif *.tiff)",
    "vector": "",
    "joblib": "Joblib files (*.joblib)"
}

class ModelKind(str, Enum):
    CLASSIFIER = "classifier"
    REGRESSOR = "regressor"


def set_placeholder_text(
    file_widget: QgsFileWidget, placeholder_text = "[Save to temporary file]"
) -> bool:
    """Tries to find QLineEdit in a QgsFileWidget and set its placeholder text."""
    line_edit = file_widget.findChild(QLineEdit)
    if line_edit:
        line_edit.setPlaceholderText(placeholder_text)
        return True
    return False


def set_filter(file_widget: QgsFileWidget, filter: Literal["raster", "vector", "joblib"]) -> bool:
    "Tries to set set specified filter to a QgsFileWidget."
    if filter in FILE_FILTERS.keys():
        file_widget.setFilter(FILE_FILTERS[filter])
        return True
    return False


def get_output_path(file_widget: QgsFileWidget) -> str:
    fp = file_widget.filePath()
    return fp if fp != "" else TEMPORARY_OUTPUT


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


def get_output_layer_name(output_raster_path: QgsFileWidget, default_output_name: str) -> str:
    if get_output_path(output_raster_path) == 'TEMPORARY_OUTPUT':
        layer_names = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
        unique_name = default_output_name
        suffix = 1
        while unique_name in layer_names:
            unique_name = f"{default_output_name}_{suffix}"
            suffix += 1
        return unique_name
    else:
        return os.path.splitext(os.path.basename(output_raster_path.filePath()))[0]


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


def apply_color_ramp_to_raster_layer(raster_layer: QgsRasterLayer, color_ramp: QgsColorRamp):
    # Don't apply color ramps for multiband raster
    if raster_layer.bandCount() > 1 or color_ramp is None:
        return

    stats = raster_layer.dataProvider().bandStatistics(1)
    shader = QgsColorRampShader(
        minimumValue=stats.minimumValue,
        maximumValue=stats.maximumValue,
        colorRamp=color_ramp
    )
    shader.classifyColorRamp()

    raster_shader = QgsRasterShader()
    raster_shader.setRasterShaderFunction(shader)
    
    renderer = QgsSingleBandPseudoColorRenderer(raster_layer.dataProvider(), 1, raster_shader)
    raster_layer.setRenderer(renderer)
    raster_layer.triggerRepaint()


def parse_string_list_parameter_and_run_command(
    algorithm: EISProcessingAlgorithm,
    parameter_index: int,
    parameters: Dict[str, QgsProcessingParameterDefinition],
    context: QgsProcessingContext,
    feedback: Optional[QgsProcessingFeedback]
) -> Dict[str, Any]:
    raw = algorithm.parameterAsString(
        parameters, algorithm.alg_parameters[parameter_index], context
    ).lower()
    values = re.split(';|,', raw)
    parameter_values = []
    for value in values:
        parameter_values.append("--" + algorithm.alg_parameters[parameter_index].replace("_", "-"))
        parameter_values.append(value) 

    # Remove parameter from the list to not prepare them again in the next step
    algorithm.alg_parameters.pop(parameter_index)
    typer_args, typer_options, output_path = algorithm.prepare_arguments(parameters, context)
    typer_options += parameter_values  # Combine lists

    toolkit_invoker = EISToolkitInvoker()
    toolkit_invoker.assemble_cli_command(algorithm.name(), typer_args, typer_options)
    results = toolkit_invoker.run_toolkit_command(feedback)

    algorithm.get_results(results, parameters)
    results["output_path"] = output_path

    feedback.setProgress(100)

    return results