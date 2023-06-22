import os
# import re
import subprocess
from typing import Dict

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingFeedback,
    QgsProcessingOutputMultipleLayers,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterCrs,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterMapLayer,
    QgsProcessingParameterMatrix,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
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

        self.alg_parameters = []

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
        args = []

        flag_mapping = {
            "resampling_method": "--resampling-method",
            "output_raster": "--output-raster-file",
            "same_extent": "--same-extent",
            "crs": "--crs",
            # Add more mappings as needed
        }

        for name in self.alg_parameters:
            param = self.parameterDefinition(name)
            flag = flag_mapping.get(name)

            if isinstance(param, QgsProcessingParameterBoolean):
                arg = str(self.parameterAsBool(parameters, name, context))

            elif isinstance(param, QgsProcessingParameterString):
                arg = self.parameterAsString(parameters, name, context)

            elif isinstance(param, QgsProcessingParameterNumber):
                if param.dataType() == QgsProcessingParameterNumber.Integer:
                    arg = str(self.parameterAsInt(parameters, name, context))
                else:
                    arg = str(self.parameterAsDouble(parameters, name, context))

            elif isinstance(param, QgsProcessingParameterMapLayer):
                layer = self.parameterAsLayer(parameters, name, context)
                arg = os.path.normpath(layer.source())

            elif isinstance(param, QgsProcessingParameterRasterLayer):
                layer = self.parameterAsRasterLayer(parameters, name, context)
                arg = os.path.normpath(layer.source())

            elif isinstance(param, QgsProcessingParameterFeatureSource):
                layer = self.parameterAsVectorLayer(parameters, name, context)
                arg = os.path.normpath(layer.source())

            elif isinstance(param, QgsProcessingParameterVectorLayer):
                layer = self.parameterAsVectorLayer(parameters, name, context)
                arg = os.path.normpath(layer.source())

            elif isinstance(param, QgsProcessingParameterMultipleLayers):
                layers = self.parameterAsLayerList(parameters, name, context)
                [args.append(os.path.normpath(layer.source())) for layer in layers]
                continue

            # TODO check if works
            elif isinstance(param, QgsProcessingParameterFile):
                arg = self.parameterAsFile(parameters, name, context)

            # TODO
            elif isinstance(param, QgsProcessingParameterEnum):
                arg = self.parameterAsEnumString(parameters, name, context)

            elif isinstance(param, QgsProcessingParameterCrs):
                crs = str(self.parameterAsCrs(parameters, name, context))
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
                    "Parameter conversion failed, parameter is unknown type"
                )

            if flag:
                args.append(flag)
            args.append(arg)

        return args

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        if feedback is None:
            feedback = QgsProcessingFeedback()

        arguments = self.prepare_arguments(parameters, context)

        eis_executable = get_python_venv_path() + "/bin/eis"
        # python_path = python_venv_path + "/bin/python"
        # toolkit_path = python_venv_path + "/lib/python3.9/site-packages/eis_toolkit/__main__.py"

        cmd = [eis_executable, (self.name() + "_cli").replace("_", "-")] + arguments
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
        )

        # TODO
        # progress_regex = re.compile(r"(\d+)%")

        # while process.poll() is None:
        #     stdout = process.stdout.readline().strip()
        #     print(f"Polling toolkit. Stdout: {stdout}")

        #     progress_match = progress_regex.search(stdout)
        #     if progress_match:
        #         progress = int(progress_match.group(1))
        #         feedback.setProgress(progress)
        #     else:
        #         print(stdout)

        #     time.sleep(0.1)

        stdout, stderr = process.communicate()

        # Handle the return code as needed
        if process.returncode != 0:
            # stderr = process.stderr.read()
            print("EIS Toolkit algorithm execution failed with error:", stderr)
        else:
            print("EIS Toolkit algorithm executed successfully!")

        # Return results
        results = {}
        for output in self.outputDefinitions():
            output_name = output.name()
            if output_name in parameters:
                results[output_name] = parameters[output_name]
            elif output.type() == "outputBoolean":
                results[output_name] = stdout.strip().lower() == "true"

        return results
