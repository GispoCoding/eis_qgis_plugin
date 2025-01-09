from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterVectorLayer,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISWeightsOfEvidenceCalculateWeights(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "weights_of_evidence_calculate_weights"
        self._display_name = "Weights of evidence calculate weights"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = "Calculate weights of spatial associations."

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_raster",
            "input_vector",
            "raster_nodata",
            "weights_type",
            "studentized_contrast_threshold",
            "arrays_to_generate",
            "output_dir",
        ]

        input_raster_param = QgsProcessingParameterRasterLayer(
            name=self.alg_parameters[0], description="Evidential raster"
        )
        self.addParameter(input_raster_param)

        input_vector_param = QgsProcessingParameterVectorLayer(
            name=self.alg_parameters[1], description="Deposits"
        )
        input_vector_param.setHelp("Vector data representing the mineral deposits or occurences point data.")
        self.addParameter(input_vector_param)

        raster_nodata_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[2],
            description="Nodata value",
            type=QgsProcessingParameterNumber.Double,
            optional=True,
        )
        raster_nodata_param.setHelp("""
            The nodata value of the input raster. If not provided, nodata is read from raster metadata."""
        )
        self.addParameter(raster_nodata_param)

        weights_type_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[3],
            description="Weights type",
            options=["unique", "categorical", "ascending", "descending"],
            defaultValue=0
        )
        weights_type_param.setHelp("""
            Unique weights does not create generalized classes and does not use a studentized contrast threshold value
            while categorical, cumulative ascending and cumulative descending do. Categorical weights are calculated so
            that all classes with studentized contrast below the defined threshold are grouped into one generalized
            class. Cumulative ascending and descending weights find the class with max contrast and group classes
            above/below into generalized classes. Generalized weights are also calculated for generalized classes."""
        )
        self.addParameter(weights_type_param)

        studentized_contrast_threshold_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4], description="Studentized contrast threshold", defaultValue=1
        )
        studentized_contrast_threshold_param.setHelp("""
            Studentized contrast threshold value used with 'categorical', 'ascending' and
            'descending' weight types. Used either as reclassification threshold directly (categorical) or to check
            that class with max contrast has studentized contrast value at least the defined value (cumulative)."""
        )
        self.addParameter(studentized_contrast_threshold_param)

        arrays_to_generate_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[5],
            description="Arrays to generate",
            options=["Class",
                     "Pixel count",
                     "Deposit count",
                     "W+",
                     "S_W+",
                     "W-",
                     "S_W-",
                     "Contrast",
                     "S_Contrast",
                     "Studentized contrast",
                     "Generalized class",
                     "Generalized W+",
                     "Generalized S_W+"
                    ],
            allowMultiple=True,
            optional=True,
        )
        arrays_to_generate_param.setHelp("""
            Arrays to generate from the computed weight metrics. Available column names for "unique" weights type are
            "Class", "Pixel count", "Deposit count", "W+", "S_W+", "W-", "S_W-", "Contrast", "S_Contrast", and
            "Studentized contrast". For other weights types, additional available column names are "Generalized class",
            "Generalzed W+", and "Generalized S_W+". Defaults to ["Class", "W+", "S_W+] for "unique" weights_type and
            ["Class", "W+", "S_W+", "Generalized W+", "Generalized S_W+"] for the cumulative weight types."""
        )
        self.addParameter(arrays_to_generate_param)

        output_dir_param = QgsProcessingParameterFolderDestination(
            name=self.alg_parameters[6], description="Output folder"
        )
        output_dir_param.setHelp("Generated arrays and a CSV of the results are saved to folder.")
        self.addParameter(output_dir_param)
    