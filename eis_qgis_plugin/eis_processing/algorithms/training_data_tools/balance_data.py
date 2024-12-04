from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterEnum,
    QgsProcessingParameterMapLayer,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISBalanceData(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "balance_data"
        self._display_name = "Balance data"
        self._group = "Training data tools"
        self._group_id = "training_data_tools"
        self._short_help_string = """
            Balances the classes of input dataset using SMOTETomek resampling method.

            For more information about Imblearn SMOTETomek read the documentation here:
            https://imbalanced-learn.org/stable/references/generated/imblearn.combine.SMOTETomek.html.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "target_labels",
            "sampling_strategy",
            "random_state",
            "output_raster",
            "output_labels"
        ]

        input_raster_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[0],
            description="Input data",
            layerType=QgsProcessing.TypeRaster,
        )
        input_raster_param.setHelp("Input data to be resampled.")
        self.addParameter(input_raster_param)

        target_labels_param = QgsProcessingParameterMapLayer(
            name=self.alg_parameters[1],
            description="Target labels"
        )
        target_labels_param.setHelp("Labels corresponding to input data.")
        self.addParameter(target_labels_param)

        sampling_strategy_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[2],
            description="Sampling strategy",
            options=["minority", "not minority", "not majority", "all", "auto"],
            defaultValue="auto"
        )
        sampling_strategy_param.setHelp(
            "Sampling strategy to use. 'minority' resamples only the minority class, 'not minority' \
            resamples all classes but the minority class, 'not majority' resamples all classes \
            but the majority class, 'all' resamples all classes and 'auto' is equivalent to 'not majority'."
        )
        self.addParameter(sampling_strategy_param)

        random_state_param = QgsProcessingParameterNumber(
            name = self.alg_parameters[3],
            description="Random state",
            optional=True,
            minValue=0
        )
        random_state_param.setHelp("Seed for random number generation.")
        self.addParameter(random_state_param)
        
        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[4],
            description="Output raster"
        )
        output_raster_param.setHelp("Resampled feature data.")
        self.addParameter(output_raster_param)

        output_labels_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[5],
            description="Output labels"
        )
        output_labels_param.setHelp("Labels corresponding to resampled feature data.")
        self.addParameter(output_labels_param)