from qgis.core import (
    QgsProcessingParameterEnum,
    QgsProcessingParameterFileDestination,
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
        self._short_help_string = "Compute weights of evidence"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "evidential_raster",
            "deposits",
            "raster_nodata",
            "weights_type",
            "studentized_contrast_threshold",
            "rasters_to_generate",
            "output_table",
            "output_raster",
        ]

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                name=self.alg_parameters[0], description="Geospatial evidence raster"
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                name=self.alg_parameters[1], description="Mineral deposits"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[2],
                description="Override raster nodata",
                type=QgsProcessingParameterNumber.Double,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[3],
                description="Weights of evidence computations type",
                options=[
                    "Unique weights",
                    "Categorical weights",
                    "Cumulative ascending weights",
                    "Cumulative descending weights",
                ],
                defaultValue=1,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[4],
                description="Studentized contrast threshold",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=2.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[5],
                description="Rasters to generate",
                options=[
                    "Class",
                    "W+",
                    "S_W+",
                    "W-",
                    "S_W-",
                    "Contrast",
                    "Studentized contrast",
                    "Generalized W+",
                    "Generalized S_W+",
                ],
                allowMultiple=True,
                defaultValue=[0, 1, 2, 7, 8],
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[6], description="Output table"
            )
        )

        self.addParameter(
            QgsProcessingParameterFolderDestination(
                name=self.alg_parameters[7], description="Output rasters"
            )
        )
