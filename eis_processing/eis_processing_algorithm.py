from typing import List, Dict
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterString,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterEnum
)


class EISProcessingAlgorithm(QgsProcessingAlgorithm):

    def __init__(self, descriptions: Dict, parameters: List[Dict]) -> None:
        super().__init__()

        self._name = descriptions['name']
        self._display_name = descriptions['display_name']
        self._group = descriptions['group']
        self._group_id = descriptions['group_id']
        self._short_help_string = descriptions['short_help']

        self.parameters = parameters  # list of dictionaries

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

    def add_parameters(self, parameters: List[Dict]):
        for param_dict in parameters:
            param_type = param_dict.pop('type')
            if param_type == 'boolean':
                self.addParameter(QgsProcessingParameterBoolean(**param_dict))
            elif param_type == 'string':
                self.addParameter(QgsProcessingParameterString(**param_dict))
            elif param_type == 'number':
                self.addParameter(QgsProcessingParameterNumber(**param_dict))
            elif param_type == 'raster':
                self.addParameter(QgsProcessingParameterRasterLayer(**param_dict))
            elif param_type == 'vector':
                self.addParameter(QgsProcessingParameterVectorLayer(**param_dict))
            elif param_type == 'multiple':
                self.addParameter(QgsProcessingParameterMultipleLayers(**param_dict))
            elif param_type == 'enum':
                self.addParameter(QgsProcessingParameterEnum(**param_dict))
            # if param['type'] == 'boolean':
            #     self.addParameter(QgsProcessingParameterBoolean(param['name'], param['description'], defaultValue=param['default']))
            # elif param['type'] == 'string':
            #     self.addParameter(QgsProcessingParameterString(param['name'], param['description'], defaultValue=param['default']))
            # elif param['type'] == 'number':
            #     self.addParameter(QgsProcessingParameterNumber(param['name'], param['description'], type=param['datatype'], defaultValue=param['default']))
            # elif param['type'] == 'raster':
            #     self.addParameter(QgsProcessingParameterRasterLayer(param['name'], param['description'], defaultValue=param['default']))
            # elif param['type'] == 'vector':
            #     self.addParameter(QgsProcessingParameterVectorLayer(param['name'], param['description'], types=param['geometry'], defaultValue=param['default']))
            # elif param['type'] == 'multiple':
            #     self.addParameter(QgsProcessingParameterMultipleLayers(param['name'], param['description'], param['datatype'], defaultValue=param['default']))
            # elif param['type'] == 'enum':
            #     self.addParameter(QgsProcessingParameterEnum(param['name'], param['description'], options=param['options'], defaultValue=param['default']))

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.add_parameters(self.parameters)

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        source = self.parameterAsSource(
            parameters,
            self.INPUT,
            context
        )

        # If source was not found, throw an exception to indicate that the algorithm
        # encountered a fatal error. The exception text can be any string, but in this
        # case we use the pre-built invalidSourceError method to return a standard
        # helper text for when a source cannot be evaluated
        if source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            source.fields(),
            source.wkbType(),
            source.sourceCrs()
        )

        # Send some information to the user
        feedback.pushInfo('CRS is {}'.format(source.sourceCrs().authid()))

        # If sink was not created, throw an exception to indicate that the algorithm
        # encountered a fatal error. The exception text can be any string, but in this
        # case we use the pre-built invalidSinkError method to return a standard
        # helper text for when a sink cannot be evaluated
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        # Compute the number of steps to display within the progress bar and
        # get features from source
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        features = source.getFeatures()

        for current, feature in enumerate(features):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break

            # Add a feature in the sink
            sink.addFeature(feature, QgsFeatureSink.FastInsert)

            # Update the progress bar
            feedback.setProgress(int(current * total))

        # To run another Processing algorithm as part of this algorithm, you can use
        # processing.run(...). Make sure you pass the current context and feedback
        # to processing.run to ensure that all temporary layer outputs are available
        # to the executed algorithm, and that the executed algorithm can send feedback
        # reports to the user (and correctly handle cancellation and progress reports!)
        if False:
            buffered_layer = processing.run("native:buffer", {
                'INPUT': dest_id,
                'DISTANCE': 1.5,
                'SEGMENTS': 5,
                'END_CAP_STYLE': 0,
                'JOIN_STYLE': 0,
                'MITER_LIMIT': 2,
                'DISSOLVE': False,
                'OUTPUT': 'memory:'
            }, context=context, feedback=feedback)['OUTPUT']

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {self.OUTPUT: dest_id}

    