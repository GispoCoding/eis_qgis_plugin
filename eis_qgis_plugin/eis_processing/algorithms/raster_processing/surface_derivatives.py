from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISSurfaceDerivatives(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "surface_derivatives"
        self._display_name = "Surface derivatives"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = """
            Calculate the selected first and/or second order surface attributes.

            For each selected surface parameter, one output raster is produced.
            
            Input raster should be a single-band raster.

            References:
                Young, M., 1978: Terrain analysis program documentation. Report 5 on Grant DA-ERO-591-73-G0040, \
                'Statistical characterization of altitude matrices by computer'. Department of Geography, \
                University of Durham, England: 27 pp.

                Zevenbergen, L.W. and Thorne, C.R., 1987: Quantitative analysis of land surface topography, \
                Earth Surface Processes and Landforms, 12: 47-56.

                Wood, J., 1996: The Geomorphological Characterisation of Digital Elevation Models. Doctoral Thesis. \
                Department of Geography, University of Leicester, England: 466 pp.

                Parameters longc and crosc from are referenced by Zevenbergen & Thorne (1987) \
                as profile and plan curvature.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "first_order_parameters",
            "second_order_parameters",
            "scaling_factor", 
            "slope_tolerance",
            "slope_gradient_unit",
            "slope_direction_unit",
            "first_order_method",
            "second_order_method",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Input raster"
        )
        input_raster_param.setHelp(
            "The input raster for surface derivative calculation. Should be a single-band raster."
        )
        self.addParameter(input_raster_param)
       
        first_order_surfce_parameters_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[1],
            options=[
                "G",
                "A"
            ],
            allowMultiple=True,
            description="First order surface parameters"
        )
        first_order_surfce_parameters_param.setHelp("The list of first order surface parameters to be calculated.")
        self.addParameter(first_order_surfce_parameters_param)

        second_order_surfce_parameters_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[2],
            options=[
                "planc",
                "profc",
                "profc_min",
                "profc_max",
                "longc",
                "crosc",
                "rot",
                "K",
                "genc",
                "tangc"
            ],
            allowMultiple=True,
            description="Second order surface parameters"
        )
        second_order_surfce_parameters_param.setHelp("The list of second order surface parameters to be calculated.")
        self.addParameter(second_order_surfce_parameters_param)

        scaling_factor_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            optional=True,
            defaultValue=1.0,
            minValue=0.00001,
            description="Scaling factor",
            type=QgsProcessingParameterNumber.Double
        )
        scaling_factor_param.setHelp(
            "The scaling factor to be applied to the raster data set. Used for both first and second \
            order parameters. Must be greater than 0."
        )
        self.addParameter(scaling_factor_param)

        slope_tolerance_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4],
            optional=True,
            defaultValue=0.0,
            description="Tolerance value",
            type=QgsProcessingParameterNumber.Double
        )
        slope_tolerance_param.setHelp(
            "The tolerance value for flat pixels. Used for both first and second order parameters."
        )
        self.addParameter(slope_tolerance_param)

        slope_gradient_unit_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[5],
            options=["radians", "degrees", "rise"],
            defaultValue=0,
            description="Slope gradient"
        )
        slope_gradient_unit_param.setHelp(
            "The unit of the slope gradient parameter. Used only for first order parameters.")
        self.addParameter(slope_gradient_unit_param)

        slope_direction_unit_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[6],
            options=["radians", "degrees"],
            defaultValue=0,
            description="Slope direction"
        )
        slope_direction_unit_param.setHelp(
            "The unit of the slope direction parameter. Used only for first order parameters."
        )
        self.addParameter(slope_direction_unit_param)

        first_order_method_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[7],
            options=["Horn", "Evans", "Young", "Zevenbergen"],
            defaultValue=0,
            description="First order method"
        )
        first_order_method_param.setHelp(
            "The method for calculating the first order coefficients."
        )
        self.addParameter(first_order_method_param)

        second_order_method_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[8],
            options=["Young", "Evans", "Zevenbergen"],
            defaultValue=0,
            description="Second order method"
        )
        second_order_method_param.setHelp(
            "The method for calculating the second order coefficients."
        )
        self.addParameter(second_order_method_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[9], description="Surface derivatives output"
        )
        output_raster_param.setHelp("The output surface derivative raster.")
        self.addParameter(output_raster_param)
 