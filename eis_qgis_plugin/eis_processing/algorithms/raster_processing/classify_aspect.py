from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISClassifyAspect(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "classify_aspect"
        self._display_name = "Classify aspect"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = """
            Classify an aspect raster data set into directional classes.

            Can classify an aspect raster into 8 or 16 equally spaced directions with \
            intervals of pi/4 and pi/8, respectively.

            Exemplary for 8 classes, the center of the intervall for North direction is 0°/360° \
            and edges are [337.5°, 22.5°], counting forward in clockwise direction. For 16 classes, \
            the intervall-width is half with edges at [348,75°, 11,25°].

            Directions and interval for 8 classes: \
            N: (337.5, 22.5), NE: (22.5, 67.5), \
            E: (67.5, 112.5), SE: (112.5, 157.5), \
            S: (157.5, 202.5), SW: (202.5, 247.5), \
            W: (247.5, 292.5), NW: (292.5, 337.5)

            Directions and interval for 16 classes: \
            N: (348.75, 11.25), NNE: (11.25, 33.75), NE: (33.75, 56.25), ENE: (56.25, 78.75), \
            E: (78.75, 101.25), ESE: (101.25, 123.75), SE: (123.75, 146.25), SSE: (146.25, 168.75), \
            S: (168.75, 191.25), SSW: (191.25, 213.75), SW: (213.75, 236.25), WSW: (236.25, 258.75), \
            W: (258.75, 281.25), WNW: (281.25, 303.75), NW: (303.75, 326.25), NNW: (326.25, 348.75) \

            Flat pixels (input value: -1) will be kept, the class is called ND (not defined).
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "unit",
            "num_classes",
            "output_raster"
        ]
    
        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("The input aspect raster to be classified.")
        self.addParameter(input_raster_param)

        unit_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[1],
            options=["degrees", "radians"],
            defaultValue=1,
            description="Unit",
        )
        unit_param.setHelp("The unit of the input raster.")
        self.addParameter(unit_param)

        num_classes_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[2],
            options=["8", "16"],
            defaultValue=0,
            description="Number of classes",
        )
        num_classes_param.setHelp("The number of classes for discretization.")
        self.addParameter(num_classes_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[3], description="Output raster"
        )
        output_raster_param.setHelp("The classified aspect raster.")
        self.addParameter(output_raster_param)
