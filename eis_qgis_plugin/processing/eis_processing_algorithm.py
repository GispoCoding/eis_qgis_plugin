import os
from typing import Any, Dict, List, Optional, Tuple

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingOutputMultipleLayers,
    QgsProcessingParameterBand,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterCrs,
    QgsProcessingParameterDefinition,
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

from .eis_toolkit_invoker import EISToolkitInvoker


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
        """
        QgsProcessingAlgorithm method.

        Returns the unique name (ID) of the processing algorithm.
        """
        return self._name

    def displayName(self):
        """
        QgsProcessingAlgorithm method.

        Returns the display name of the processing algorithm.
        """
        return self._display_name

    def group(self):
        """
        QgsProcessingAlgorithm method.

        Returns the display name of the group the processing algorithm belongs to.
        """
        return self._group

    def groupId(self):
        """
        QgsProcessingAlgorithm method.

        Returns the group ID of the processing algorithm.
        """
        return self._group_id

    def shortHelpString(self):
        """
        QgsProcessingAlgorithm method.

        Returns the short help string of the processing algorithm.
        """
        return self._short_help_string

    def createInstance(self):
        """
        QgsProcessingAlgorithm method.

        Creates instance of the processing algorithm class.
        """
        return self.__class__()

    def initAlgorithm(self, config=None):
        """
        QgsProcessingAlgorithm method.

        Initializes the algorithm by defining its parameters. Implemented in child
        classes for EISProcessingAlgorithms.
        """
        raise Exception("initAlgorithm is not implemented in the child class!")

    def prepare_arguments(
        self,
        parameters: Dict[str, QgsProcessingParameterDefinition],
        context: QgsProcessingContext
    ) -> Tuple[List[str], List[str]]:
        """
        Prepare arguments to call EIS Toolkit CLI.

        Iterates all parameters of the algorithm and creates command-line arguments
        to be delivered to EIS Toolkit. Most parameter values are delivered with their
        name as Typer options.

        See https://typer.tiangolo.com/ for more information about the used CLI package.

        Returns:
            List of arguments (a list with only parameter values, non-empty only if
            QgsProcessingParameterMultipleLayers is present) and list where every other element is
            parameter name and every other is the parameter value (of the preceding parameter name).
        """

        typer_args = []  # These parameters are delivered without the parameter name tag (as Typer arguments)
        typer_options = []  # These parameters are delivered with their name ()

        # By default, all parameters are passed as Typer options (parameter name needs to be delivered
        # prefixed with --)

        # TODO: Check if all these work with optional parameters (param_value evaluating to None)

        for name in self.alg_parameters:
            param = self.parameterDefinition(name)
            param_name = "--" + name.replace("_", "-")

            if isinstance(param, QgsProcessingParameterBand):
                param_value = str(self.parameterAsInt(parameters, name, context))

            elif isinstance(param, QgsProcessingParameterBoolean):
                if self.parameterAsBool(parameters, name, context):
                    typer_options.append(param_name)
                else:
                    typer_options.append(param_name[:2] + "no-" + param_name[2:])
                continue

            elif isinstance(param, QgsProcessingParameterString):
                param_value = self.parameterAsString(parameters, name, context).lower()

            elif isinstance(param, QgsProcessingParameterNumber):
                if not self.parameterAsString(parameters, name, context):  # param_value is None
                    continue
                if param.dataType() == QgsProcessingParameterNumber.Integer:
                    param_value = str(self.parameterAsInt(parameters, name, context))
                else:
                    param_value = str(self.parameterAsDouble(parameters, name, context))

            elif isinstance(param, QgsProcessingParameterExtent):
                if not self.parameterAsString(parameters, name, context):  # param_value is None
                    continue
                extents = (
                    self.parameterAsString(parameters, name, context)
                    .split("[")[0]
                    .strip()
                    .split(",")
                )
                typer_options.append(param_name)
                [typer_options.append(coord) for coord in extents]
                continue

            elif isinstance(param, QgsProcessingParameterField):
                if param.allowMultiple():
                    fields = self.parameterAsFields(parameters, name, context)
                    for field in fields:
                        typer_args.append(param_name)
                        typer_args.append(field)
                    continue
                else:
                    param_value = self.parameterAsString(parameters, name, context)

            elif isinstance(param, QgsProcessingParameterMapLayer):
                layer = self.parameterAsLayer(parameters, name, context)
                if not layer:
                    continue
                param_value = os.path.normpath(layer.source())

            elif isinstance(param, QgsProcessingParameterRasterLayer):
                layer = self.parameterAsRasterLayer(parameters, name, context)
                if not layer:
                    continue
                param_value = os.path.normpath(layer.source())

            elif isinstance(param, QgsProcessingParameterFeatureSource):
                layer = self.parameterAsVectorLayer(parameters, name, context)
                if not layer:
                    continue
                param_value = os.path.normpath(layer.source())

            elif isinstance(param, QgsProcessingParameterVectorLayer):
                layer = self.parameterAsVectorLayer(parameters, name, context)
                if not layer:
                    continue
                param_value = os.path.normpath(layer.source())

            # Multiple layers input needs to be the first delivered to the CLI always
            elif isinstance(param, QgsProcessingParameterMultipleLayers):
                layers = self.parameterAsLayerList(parameters, name, context)
                if not layers:
                    continue
                [typer_args.append(os.path.normpath(layer.source())) for layer in layers]
                continue

            # TODO check if works
            elif isinstance(param, QgsProcessingParameterPoint):
                coords = self.parameterAsPoint(parameters, name, context)
                if not coords:
                    continue
                typer_options.append(param_name)
                typer_options.append(str(coords.x()))
                typer_options.append(str(coords.y()))
                continue

            # TODO check if works
            elif isinstance(param, QgsProcessingParameterFile):
                param_value = self.parameterAsFile(parameters, name, context)

            # TODO
            elif isinstance(param, QgsProcessingParameterEnum):
                if param.allowMultiple():
                    indices = self.parameterAsEnums(parameters, name, context)
                    for idx in indices:
                        typer_options.append(param_name)
                        typer_options.append(param.options()[idx])
                    continue
                else:
                    # The following bugged in some QGIS v?
                    # param_value = self.parameterAsEnumString(parameters, name, context)
                    idx = self.parameterAsEnum(parameters, name, context)
                    param_value = param.options()[idx]
                    # NOTE: converting values to lowercase removed, algs will need to be updated
                    # if len(param_value) > 1:
                    #     param_value = param_value.lower()

            elif isinstance(param, QgsProcessingParameterCrs):
                crs = str(self.parameterAsCrs(parameters, name, context))
                if not crs:
                    continue
                param_value = str(crs.split("EPSG:")[-1][:-1])

            # TODO (remove? broken parameter type in some API versions)
            elif isinstance(param, QgsProcessingParameterMatrix):
                param_value = [
                    str(item)
                    for item in self.parameterAsMatrix(parameters, name, context)
                ]

            elif isinstance(
                param, QgsProcessingParameterRasterDestination
            ) or isinstance(param, QgsProcessingParameterVectorDestination):
                param_value = os.path.normpath(
                    self.parameterAsOutputLayer(parameters, name, context)
                )

            # TODO
            elif isinstance(param, QgsProcessingParameterFeatureSink):
                raise Exception("Not implemented yet")

            # TODO
            elif isinstance(param, QgsProcessingOutputMultipleLayers):
                param_value = self.parameterAsLayerList
                raise Exception("Not implemented yet")

            elif isinstance(param, QgsProcessingParameterFileDestination):
                param_value = os.path.normpath(
                    self.parameterAsFileOutput(parameters, name, context)
                )

            elif isinstance(param, QgsProcessingParameterFolderDestination):
                param_value = os.path.normpath(
                    self.parameterAsString(parameters, name, context)
                )
                # Create the folder if it doesn't exist. TBD if this is the best practice
                if not os.path.exists(param_value):
                    os.makedirs(param_value)

            else:
                raise Exception(
                    f"Parameter ({param_name}) conversion failed, parameter is unknown type."
                )

            if not param_value:
                continue

            # NOTE: Attempt to exclude some extra details that might come with layer file path for example
            if "|" in param_value:
                param_value = param_value.split("|")[0]

            typer_options.append(param_name)
            typer_options.append(param_value)

        return typer_args, typer_options


    def get_results(self, results: dict, parameters: Dict[str, QgsProcessingParameterDefinition]):
        for output in self.outputDefinitions():
            output_name = output.name()
            if output_name in parameters:
                results[output_name] = parameters[output_name]
            elif output.type() == "outputBoolean":
                results[output_name] = results["result"]


    def processAlgorithm(
        self,
        parameters: Dict[str, QgsProcessingParameterDefinition],
        context: QgsProcessingContext,
        feedback: Optional[QgsProcessingFeedback]
    ) -> Dict[str, Any]:
        """
        QgsProcessingAlgorithm method.

        Defined commonly for all EISProcessingAlgorithms. A command to EIS Toolkit CLI is
        constructed using `prepare_arguments` and `assemble_cli_call` of EISToolkitInvoker.
        
        EISToolkitInvoker will handle the actual communication with EIS Toolkit.
        """

        if feedback is None:
            feedback = QgsProcessingFeedback()

        typer_args, typer_options = self.prepare_arguments(parameters, context)
        
        toolkit_invoker = EISToolkitInvoker()
        toolkit_invoker.assemble_cli_command(self.name(), typer_args, typer_options)
        results = toolkit_invoker.run_toolkit_command(feedback)

        self.get_results(results, parameters)

        return results
