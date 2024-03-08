from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISFocalFilter(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "focal_filter"
        self._display_name = "Focal filter"
        self._group = "Filtering"
        self._group_id = "filtering"
        self._short_help_string = "Apply a basic focal filter to the input raster"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "method",
            "size",
            "shape",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Input raster"
            )
        input_raster_param.setHelp("The input raster data set.")
        self.addParameter(input_raster_param)
       
        method_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[1],
            description="Method",
            options=["mean", "median"],
            defaultValue="mean",
        )
        method_param.setHelp(
            "The method to use for filtering. Can be either 'mean' or 'median'."
        )
        self.addParameter(method_param)

        size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Size",
            minValue=1,
            defaultValue=3,
        )
        size_param.setHelp(
            "The size of the filter window. E.g., 3 means a 3x3 window."
        )
        self.addParameter(size_param)
           
        shape_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[3],
            description="Shape",
            options=["circle", "square"],
            defaultValue="circle",
        )
        shape_param.setHelp(
            "The shape of the filter window. Can be either 'square' or 'circle'."
        )
        self.addParameter(shape_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[4], description="Output raster"
        )
        output_raster_param.setHelp("The output raster data set.")
        self.addParameter(output_raster_param)
