import os
import subprocess
import time

from typing import List, Dict

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterMapLayer, # Not needed?
    QgsProcessingParameterBoolean,
    QgsProcessingParameterString,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterFile,
    QgsProcessingParameterEnum,
    QgsProcessingParameterMatrix,
    QgsProcessingParameterCrs,
    QgsProcessingFeedback,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterFileDestination,
    QgsProcessingOutputMultipleLayers
)


# NOTE:
# While these paths exist within the script, modify them to correspond to your Python venv and interface file location
PYTHON_SCRIPT_FOLDER_PATH = "/home/niko/code/eis_venv"
PYTOHN_PATH = PYTHON_SCRIPT_FOLDER_PATH + "/bin/python"
TOOLKIT_PATH = PYTHON_SCRIPT_FOLDER_PATH + "/lib/python3.9/site-packages/eis_toolkit/wizard_interface/toolkit_interface_arg_parsing.py"


class EISProcessingAlgorithm(QgsProcessingAlgorithm):

    def __init__(self, descriptions: Dict[str, str], params: List[Dict[str, str]]) -> None:
        super().__init__()

        self.descriptions = descriptions  # dict
        self.params = params  # list of dictionaries

        self._name = descriptions['name']
        self._display_name = descriptions['display_name']
        self._group = descriptions['group']
        self._group_id = descriptions['group_id']
        self._short_help_string = descriptions['short_help']

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
        return self.__class__(self.descriptions, self.params)

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        for param_dict in self.params: 
            param_type = param_dict['type']
            # Copy the dict because we modify the dict below
            param_dict_copy = param_dict.copy()
            param_dict_copy.pop('type')
            if param_type == 'boolean':
                self.addParameter(QgsProcessingParameterBoolean(**param_dict_copy))
            elif param_type == 'string':
                self.addParameter(QgsProcessingParameterString(**param_dict_copy))
            elif param_type == 'number':
                if 'num_type' in param_dict_copy.keys() and param_dict_copy.pop('num_type') == 'double':
                    param_dict_copy['type'] = QgsProcessingParameterNumber.Double
                self.addParameter(QgsProcessingParameterNumber(**param_dict_copy))
            elif param_type == 'file':
                # TODO: is there a need to specify extension as a param?
                self.addParameter(QgsProcessingParameterFile(**param_dict_copy))
            elif param_type == 'raster':
                self.addParameter(QgsProcessingParameterRasterLayer(**param_dict_copy))
            elif param_type == 'vector':
                self.addParameter(QgsProcessingParameterVectorLayer(**param_dict_copy))
            elif param_type == 'source':
                self.addParameter(QgsProcessingParameterFeatureSource(**param_dict_copy))
            elif param_type == 'multiple':
                self.addParameter(QgsProcessingParameterMultipleLayers(**param_dict_copy))
            elif param_type == 'enum':
                param_dict_copy['options'] = [opt.strip() for opt in param_dict_copy['options'].split("|")]
                self.addParameter(QgsProcessingParameterEnum(**param_dict_copy))
            elif param_type == 'crs':
                self.addParameter(QgsProcessingParameterCrs(**param_dict_copy))
            elif param_type == 'matrix':
                self.addParameter(QgsProcessingParameterMatrix(**param_dict_copy))
                # NOTE: causes QGIS to crash?
            elif param_type == 'raster_out':
                self.addParameter(QgsProcessingParameterRasterDestination(**param_dict_copy))
            elif param_type == 'vector_out':
                self.addParameter(QgsProcessingParameterVectorDestination(**param_dict_copy))
            elif param_type == 'file_out':
                self.addParameter(QgsProcessingParameterFileDestination(**param_dict_copy))
            else:
                raise Exception("Invalid parameter type in config file")

    def convert_parameters(self, parameters: Dict, context):
        converted_parameters = []
        for name, _ in parameters.items():
            param = self.parameterDefinition(name)
            if isinstance(param, QgsProcessingParameterBoolean):
                converted_param = str(self.parameterAsBool(parameters, name, context))

            elif isinstance(param, QgsProcessingParameterString):
                converted_param = self.parameterAsString(parameters, name, context)

            elif isinstance(param, QgsProcessingParameterNumber):
                if param.dataType() == QgsProcessingParameterNumber.Integer:
                    converted_param = str(self.parameterAsDouble(parameters, name, context))
                else:
                    converted_param = str(self.parameterAsDouble(parameters, name, context))

            elif isinstance(param, QgsProcessingParameterRasterLayer):
                layer = self.parameterAsRasterLayer(parameters, name, context)
                converted_param = os.path.normpath(layer.source())

            elif isinstance(param, QgsProcessingParameterVectorLayer):
                layer = self.parameterAsVectorLayer(parameters, name, context)
                converted_param = os.path.normpath(layer.source())

            elif isinstance(param, QgsProcessingParameterMultipleLayers):
                layers = self.parameterAsLayerList(parameters, name, context)
                # Is this okay and needed?
                if layers is None or len(layers) == 0:
                    continue
                raise Exception("Not implemented yet")
                # TODO

            elif isinstance(param, QgsProcessingParameterEnum):
                converted_param = str(self.parameterAsEnum(parameters, name, context))

            elif isinstance(param, QgsProcessingParameterMatrix):
                converted_param = [str(item) for item in self.parameterAsMatrix(parameters, name, context)]

            elif isinstance(param, QgsProcessingParameterRasterDestination) or \
               isinstance(param, QgsProcessingParameterVectorDestination):
                converted_param = os.path.normpath(self.parameterAsOutputLayer(parameters, name, context))

            elif isinstance(param, QgsProcessingParameterFileDestination):
                converted_param = os.path.normpath(self.parameterAsFileOutput(parameters, name, context))

            elif isinstance(param, QgsProcessingOutputMultipleLayers):
                converted_param = self.parameterAsLayerList
                # TODO
                raise Exception("Not implemented yet")

            else:
                raise Exception("Parameter conversion failed, parameter is unknown type")

            converted_parameters.append(param.name() + ":" + converted_param)

        return converted_parameters


    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        if feedback is None:
            feedback = QgsProcessingFeedback()

        parameters = self.convert_parameters(parameters, context)

        # Start the external process
        process = subprocess.Popen(
            [PYTOHN_PATH, TOOLKIT_PATH] + ["call_" + self.name()] + parameters,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        # Read the output of the process continuously
        # NOTE: Not sure if the polling/progress updating works now
        while process.poll() is None:
            stdout = process.stdout.readline().decode().strip()
            print(f"Polling toolkit. Stdout: {stdout}")
            if stdout and stdout[-1] == "%":
                # Parse the progress from the output
                progress = int(stdout[:-1])
                feedback.setProgress(progress)
                # feedback.setProgressText("Step %d" % i)
            else:
                print(stdout)

            time.sleep(0.1)

        # Get the return code of the process
        return_code = process.returncode

        # Handle the return code as needed
        if return_code != 0:
            stderr = process.stderr.read().decode()
            print("Error:", stderr)
        else:
            print("Success")

        results = {}
        for output in self.outputDefinitions():
            outputName = output.name()
            if outputName in parameters:
                results[outputName] = parameters[outputName]

        return results
