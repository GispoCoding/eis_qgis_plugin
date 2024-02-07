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
        self._display_name = "Surface Derivatives"
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

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[1], description="Output raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[2],
                options=["G", "A"],
                description="List of surface parameters to be calculated.",
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[3],
                optional=True,
                defaultValue=1,
                description="Scaling factor to be applied to the raster data set. Default to 1.",
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[4],
                optional=True,
                defaultValue=0,
                description="Tolerance value for flat pixels. Default to 0.",
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[5],
                options=["radians", "degrees", "rise"],
                defaultValue="radians",
                description="Unit of the slope gradient parameter. Default to radians.",
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[6],
                options=["radians", "degrees"],
                defaultValue="radians",
                description="Unit of the slope direction parameter. Default to radians.",
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[7],
                options=["Horn", "Evans", "Young", "Zevenbergen"],
                defaultValue="Horn",
                description="Method for calculating the coefficients. Default to the Horn (1981) method.",
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[8],
                options=["Young", "Evans", "Zevenbergen"],
                defaultValue="Young",
                description="Method for calculating the coefficients. Default to the Young (1978) method.",
            )
        )