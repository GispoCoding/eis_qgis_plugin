from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterEnum,
    QgsProcessingParameterMapLayer,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISLogisticRegression(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "logistic_regression_train"
        self._display_name = "Logistic regression"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = "Train a logistic regression model"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "target_labels",
            "validation_method",
            "validation_metric",
            "split_size",
            "cv_folds",
            "penalty",
            "max_iter",
            "solver",
            "verbose",
            "random_state",
            "output_file"
        ]

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                name=self.alg_parameters[0], description="Training data", layerType=QgsProcessing.TypeRaster
            )
        )

        self.addParameter(
            QgsProcessingParameterMapLayer(
                name=self.alg_parameters[1], description="Target labels"
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[2],
                description="Validation method",
                options=["split", "kfold_cv", "skfold_cv", "loo_cv", "none"],
                defaultValue="split"
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[3],
                description="Validation metric",
                options=["accuracy", "precision", "recall", "f1", "auc"],
                defaultValue="accuracy"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[4],
                description="Split size",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.2
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[5],
                description="CV folds",
                defaultValue=5
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[6],
                description="Penalty",
                options=["l2", "l1", "elasicnet"],
                defaultValue="l2",
                optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[7],
                description="Max iter",
                defaultValue=100
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[8],
                description="Solver",
                options=["lbfgs", "liblinear", "newton-cg", "newton-cholesky", "sag", "saga"],
                defaultValue="lbfgs"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[9],
                description="Verbose",
                defaultValue=0,
                minValue=0,
                maxValue=2
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[10],
                description="Random state",
                optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                name=self.alg_parameters[11],
                description="Output raster",
            )
        )
