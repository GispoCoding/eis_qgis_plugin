from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISSurfaceDerivatives(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "surface derivatives"
        self._display_name = "Surface derivatives"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Calculate the first and/or second order surface attributes."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "output_raster",
            "parameters",
            "scaling_factor", 
            "slope_tolerance",
            "slope_gradient_unit",
            "slope_direction_unit",
            "first_order_method",
            "second_order_method"
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp("The input raster data set.")
        self.addParameter(input_raster_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[1], description="Output raster"
        )
        output_raster_param.setHelp("The output raster data set.")
        self.addParameter(output_raster_param)

        surfce_parameters_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[2],
            options=["G", "A"],
            description="Surface parameters"
        )
        surfce_parameters_param.setHelp("The list of surface parameters to be calculated.")
        self.addParameter(surfce_parameters_param)

        scaling_factor_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            optional=True,
            defaultValue=1,
            description="Scaling factor"
        )
        scaling_factor_param.setHelp("The scaling factor to be applied to the raster data set. Defaults to 1.")
        self.addParameter(scaling_factor_param)

        slope_tolerance_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4],
            optional=True,
            defaultValue=0,
            description="Tolerance value"
        )
        slope_tolerance_param.setHelp("The tolerance value for flat pixels. Defaults to 0.")
        self.addParameter(slope_tolerance_param)

        slope_gradient_unit_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[5],
            options=["radians", "degrees", "rise"],
            defaultValue="radians",
            description="Slope gradient"
        )
        slope_gradient_unit_param.setHelp("The unit of the slope gradient parameter. Defaults to radians.")
        self.addParameter(slope_gradient_unit_param)

        slope_direction_unit_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[6],
            options=["radians", "degrees"],
            defaultValue="radians",
            description="Slope direction"
        )
        slope_direction_unit_param.setHelp("The unit of the slope direction parameter. Defaults to radians.")
        self.addParameter(slope_direction_unit_param)

        first_order_method_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[7],
            options=["Horn", "Evans", "Young", "Zevenbergen"],
            defaultValue="Horn",
            description="First order method"
        )
        first_order_method_param.setHelp("The method for calculating the first order coefficients. Defaults to the Horn (1981) method.")
        self.addParameter(first_order_method_param)

        second_order_method_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[8],
            options=["Young", "Evans", "Zevenbergen"],
            defaultValue="Young",
            description="Second order method"
        )
        second_order_method_param.setHelp("The method for calculating the second order coefficients. Defaults to the Young (1978) method.")
        self.addParameter(second_order_method_param)
