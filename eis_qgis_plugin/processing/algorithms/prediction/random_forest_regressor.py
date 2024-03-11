from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterMapLayer,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISRandomForestRegressor(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "random_forest_regressor_train"
        self._display_name = "Random forest regressor"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = "Train a random forest regressor model"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "target_labels",
            "validation_method",
            "validation_metric",
            "split_size",
            "cv_folds",
            "n_estimators",
            "criterion",
            "max_depth",
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
                options=["mse", "rmse", "mae", "r2"],
                defaultValue="mse"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[4],
                description="Split size",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.2,
                minValue=0.001,
                maxValue=0.999
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[5],
                description="CV folds",
                defaultValue=5,
                minValue=2
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[6],
                description="N estimators",
                defaultValue=100,
                minValue=1
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.alg_parameters[7],
                description="Criterion",
                options=["squared_error", "absolute_error", "friedman_mse", "poisson"],
                defaultValue="squared_error"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[8],
                description="Max depth",
                optional=True,
                minValue=1
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
                optional=True,
                minValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[11],
                description="Output model",
                fileFilter='.joblib (*.joblib)'
            )
        )
