import json
import os
import subprocess
import time
from typing import Dict, List

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingFeedback,
    QgsProcessingOutputMultipleLayers,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterCrs,
    QgsProcessingParameterEnum,
    QgsProcessingParameterExtent,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterMapLayer,
    QgsProcessingParameterMatrix,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterPoint,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterString,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.settings import get_python_venv_path


class EISProcessingAlgorithm(QgsProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = ""
        self._display_name = ""
        self._group = ""
        self._group_id = ""
        self._short_help_string = ""

        self.alg_parameters: List[str] = []

    def name(self):
        return self._name

    def displayName(self):
        return self._display_name

    def group(self):
        return self._group

    def groupId(self):
        return self._group_id

    def shortHelpString(self):
        return self._short_help_string

    def createInstance(self):
        return self.__class__()

    def initAlgorithm(self, config=None):
        raise Exception("Not implemented in the child class!")

    def prepare_arguments(self, parameters: Dict, context):
        args = []  # These parameters are delivered without the parameter name tag
        kwargs = []  # These parameters are delivered with their name

        # By default, all parameters are passed as Typer options (parameter name needs to be delivered
        # prefixed with --)

        # TODO: Check if all these work with optional parameters (arg evaluating to None)

        # NOTE: Because of the above, flag mapping is likely to be deleted
        # flag_mapping = {
        #     "resampling_method": "--resampling-method",
        #     "output_raster": "--output-raster-file",
        #     "same_extent": "--same-extent",
        #     "crs": "--crs",
        #     # Add more mappings as needed
        # }

        for name in self.alg_parameters:
            param = self.parameterDefinition(name)
            param_name = "--" + name.replace("_", "-")
            # flag = flag_mapping.get(name)
            if isinstance(param, QgsProcessingParameterBoolean):
                if self.parameterAsBool(parameters, name, context):
                    kwargs.append(param_name)
                else:
                    kwargs.append(param_name[:2] + "no-" + param_name[2:])
                continue

            elif isinstance(param, QgsProcessingParameterString):
                arg = self.parameterAsString(parameters, name, context).lower()

            elif isinstance(param, QgsProcessingParameterNumber):
                if not self.parameterAsString(parameters, name, context):  # Arg is None
                    continue
                if param.dataType() == QgsProcessingParameterNumber.Integer:
                    arg = str(self.parameterAsInt(parameters, name, context))
                else:
                    arg = str(self.parameterAsDouble(parameters, name, context))

            elif isinstance(param, QgsProcessingParameterExtent):
                if not self.parameterAsString(parameters, name, context):  # Arg is None
                    continue
                extents = (
                    self.parameterAsString(parameters, name, context)
                    .split("[")[0]
                    .strip()
                    .split(",")
                )
                kwargs.append(param_name)
                [kwargs.append(coord) for coord in extents]
                continue

            elif isinstance(param, QgsProcessingParameterField):
                arg = self.parameterAsString(parameters, name, context)

            elif isinstance(param, QgsProcessingParameterMapLayer):
                layer = self.parameterAsLayer(parameters, name, context)
                if not layer:
                    continue
                arg = os.path.normpath(layer.source())

            elif isinstance(param, QgsProcessingParameterRasterLayer):
                layer = self.parameterAsRasterLayer(parameters, name, context)
                if not layer:
                    continue
                arg = os.path.normpath(layer.source())

            elif isinstance(param, QgsProcessingParameterFeatureSource):
                layer = self.parameterAsVectorLayer(parameters, name, context)
                if not layer:
                    continue
                arg = os.path.normpath(layer.source())

            elif isinstance(param, QgsProcessingParameterVectorLayer):
                layer = self.parameterAsVectorLayer(parameters, name, context)
                if not layer:
                    continue
                arg = os.path.normpath(layer.source())

            # Multiple layers input needs to be the first delivered to the CLI always
            elif isinstance(param, QgsProcessingParameterMultipleLayers):
                layers = self.parameterAsLayerList(parameters, name, context)
                if not layers:
                    continue
                [args.append(os.path.normpath(layer.source())) for layer in layers]
                continue

            # TODO check if works
            elif isinstance(param, QgsProcessingParameterPoint):
                coords = self.parameterAsPoint(parameters, name, context)
                if not coords:
                    continue
                kwargs.append(param_name)
                kwargs.append(str(coords.x()))
                kwargs.append(str(coords.y()))
                continue

            # TODO check if works
            elif isinstance(param, QgsProcessingParameterFile):
                arg = self.parameterAsFile(parameters, name, context)

            # TODO
            elif isinstance(param, QgsProcessingParameterEnum):
                arg = self.parameterAsEnumString(parameters, name, context).lower()

            elif isinstance(param, QgsProcessingParameterCrs):
                crs = str(self.parameterAsCrs(parameters, name, context))
                if not crs:
                    continue
                arg = str(crs.split("EPSG:")[-1][:-1])

            # TODO (remove? broken parameter type in some API versions)
            elif isinstance(param, QgsProcessingParameterMatrix):
                arg = [
                    str(item)
                    for item in self.parameterAsMatrix(parameters, name, context)
                ]

            elif isinstance(
                param, QgsProcessingParameterRasterDestination
            ) or isinstance(param, QgsProcessingParameterVectorDestination):
                arg = os.path.normpath(
                    self.parameterAsOutputLayer(parameters, name, context)
                )

            # TODO
            elif isinstance(param, QgsProcessingParameterFeatureSink):
                raise Exception("Not implemented yet")

            # TODO
            elif isinstance(param, QgsProcessingOutputMultipleLayers):
                arg = self.parameterAsLayerList
                raise Exception("Not implemented yet")

            elif isinstance(param, QgsProcessingParameterFileDestination):
                arg = os.path.normpath(
                    self.parameterAsFileOutput(parameters, name, context)
                )

            # TODO
            elif isinstance(param, QgsProcessingParameterFolderDestination):
                raise Exception("Not implemented yet")

            else:
                raise Exception(
                    f"Parameter ({param_name}) conversion failed, parameter is unknown type."
                )

            # if flag:
            #     args.append(flag)
            if not arg:
                continue

            # NOTE: Attempt to exclude some extra details that might come with layer file path for example
            if "|" in arg:
                arg = arg.split("|")[0]

            kwargs.append(param_name)
            kwargs.append(arg)

        return args, kwargs

    def get_bin_folder(self):
        if os.name == "nt":  # Windows
            return "Scripts"
        else:
            return "bin"

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        if feedback is None:
            feedback = QgsProcessingFeedback()

        arguments, arguments_with_name = self.prepare_arguments(parameters, context)
        eis_executable = os.path.join(
            get_python_venv_path(), self.get_bin_folder(), "eis"
        )
        cmd = [eis_executable, (self.name() + "_cli").replace("_", "-")] + arguments + arguments_with_name
        results = {}

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            # progress_regex = re.compile(r"(\d+)%")
            progress_prefix = "Progress:"
            results_prefix = "Results:"

            while process.poll() is None:
                stdout = process.stdout.readline().strip()

                # progress_match = progress_regex.search(stdout)
                # if progress_match:
                if progress_prefix in stdout:
                    # progress = int(progress_match.group(1))
                    progress = int(stdout.split(":")[1].strip()[:-1])
                    feedback.setProgress(progress)
                    feedback.pushInfo(f"Progress: {progress}%")
                elif results_prefix in stdout:
                    # Extract the JSON part
                    json_str = stdout.split(results_prefix)[-1].strip()

                    # Deserialize the JSON-formatted string to a Python dict
                    output_dict = json.loads(json_str)

                    for key, value in output_dict.items():
                        results[key] = value
                else:
                    feedback.pushInfo(stdout)

                time.sleep(0.05)

            stdout, stderr = process.communicate()

            if process.returncode != 0:
                feedback.reportError(
                    f"EIS Toolkit algorithm execution failed with error: {stderr}"
                )
            else:
                feedback.pushInfo("EIS Toolkit algorithm executed successfully!")

        except Exception as e:
            feedback.reportError(f"Failed to run the command. Error: {str(e)}")
            try:
                process.terminate()
            except UnboundLocalError:
                pass
            return {}

        # Fetch results
        for output in self.outputDefinitions():
            output_name = output.name()
            if output_name in parameters:
                results[output_name] = parameters[output_name]
            elif output.type() == "outputBoolean":
                results[output_name] = stdout.strip().lower() == "true"

        return results
