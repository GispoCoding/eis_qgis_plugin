from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISSecondOrderBasicSet(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "second order surface attributes"
        self._display_name = "Second Order Surface Attributes"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Calculate the second order surface attributes."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["raster", "parameters", "scaling_factor", "slope_tolerance", "method"]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[1],
                options=["planc", "profc", "profc_min", "profc_max", "longc", "crosc", "rot", "K", "genc", "tangc"],
                description="List of surface parameters to be calculated.",
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2],
                optional=True,
                defaultValue=1,
                description="Scaling factor to be applied to the raster data set. Default to 1.",
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[3],
                optional=True,
                defaultValue=0,
                description="Tolerance value for flat pixels. Default to 0.",
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[4],
                options=["Evans", "Young", "Zevenbergen"],
                defaultValue="Young",
                description="Method for calculating the coefficients. Default to the Young (1978) method.",
            )
        )