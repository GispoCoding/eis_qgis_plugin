from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISProximityToAnomaly(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "proximity_to_anomaly"
        self._display_name = "Proximity to anomaly"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = """
        Calculate proximity from each raster cell to nearest anomaly cell.
        
        Scales output raster values linearly based on given `max_distance_value` and `anomaly_value`.

        If 'in_between' or 'outside' is used for threshold criteria, both threshold criteria \
        value need to be provided.

        Uses only the first band of the raster.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "threshold_criteria",
            "first_threshold_criteria_value",
            "second_threshold_criteria_value",
            "max_distance",
            "max_distance_value",
            "anomaly_value",
            "output_raster",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0],
            description="Input raster",
        )
        input_raster_param.setHelp("Input anomaly raster.")
        self.addParameter(input_raster_param)

        threshold_criteria_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[1],
            description="Threshold criteria",
            options=[
                "higher",
                "lower",
                "in_between",
                "outside"
            ],
            defaultValue=0,
        )
        threshold_criteria_param.setHelp(
            "Determines how anomalous cells are defined together with threshold criteria values."
        )
        self.addParameter(threshold_criteria_param)

        first_threshold_criteria_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="First threshold criteria value",
            type=QgsProcessingParameterNumber.Double,
        )
        first_threshold_criteria_value_param.setHelp(
            "Value used to define anomalous cells. If the threshold criteria is 'lower' or 'higher', \
            only this is needed in the computations."
        )
        self.addParameter(first_threshold_criteria_value_param)

        second_threshold_criteria_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[3],
            description="Second threshold criteria value",
            type=QgsProcessingParameterNumber.Double,
            optional=True
        )
        second_threshold_criteria_value_param.setHelp(
            "The second value used to define anomalous cells. Needed when threshold criteria is either \
            'in_between' or 'outside'.."
        )
        self.addParameter(second_threshold_criteria_value_param)

        max_distance_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4],
            description="Max distance",
            type=QgsProcessingParameterNumber.Double,
            minValue=0.0
        )
        max_distance_param.setHelp("Maximum distance in the output raster.")
        self.addParameter(max_distance_param)

        max_distance_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[5],
            description="Max distance value",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=0.0
        )
        max_distance_value_param.setHelp(
            "Value at and beyond given max distance. Used for scaling the output raster values."
        )
        self.addParameter(max_distance_value_param)

        anomaly_value_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[6],
            description="Anomaly value",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=1.0
        )
        anomaly_value_param.setHelp("Value at anomaly. Used for scaling the output raster values.")
        self.addParameter(anomaly_value_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[7], description="Proximity to anomaly output"
        )
        output_raster_param.setHelp("Output raster with proximities to closest anomalies.")
        self.addParameter(output_raster_param)
