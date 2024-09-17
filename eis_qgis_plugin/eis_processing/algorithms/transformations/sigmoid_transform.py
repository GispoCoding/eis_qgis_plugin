from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISSigmoidTransform(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "sigmoid_transform"
        self._display_name = "Sigmoid transform"
        self._group = "Transformations"
        self._group_id = "transformations"
        self._short_help_string = """
            Transform data into a sigmoid-shape based on a specified new range.

            Uses the provided new minimum and maximum, shift and slope parameters to transform the data.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "limit_lower",
            "limit_upper",
            "slope",
            "center",
            "output_raster",
        ]
        
        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("Input raster to be transformed.")
        self.addParameter(input_raster_param)

        lower_limit_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Lower",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=0.0,
        )
        lower_limit_param.setHelp("Lower boundary for the calculation of the sigmoid function.")
        self.addParameter(lower_limit_param)

        upper_limit_param =  QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Upper",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=1.0,
        )
        upper_limit_param.setHelp("Upper boundary for the calculation of the sigmoid function.")
        self.addParameter(upper_limit_param)

        slope_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            description="Slope",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=1.0,
        )
        slope_param.setHelp("Value which modifies the slope of the resulting sigmoid-curve.")
        self.addParameter(slope_param)

        center_param = QgsProcessingParameterBoolean(
            name=self.alg_parameters[4], description="Center", defaultValue=True
        )
        center_param.setHelp("If array values should be centered around mean = 0 before sigmoid transformation.")
        self.addParameter(center_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[5], description="Output raster"
        )
        output_raster_param.setHelp("Output raster with the transformed data.")
        self.addParameter(output_raster_param)
