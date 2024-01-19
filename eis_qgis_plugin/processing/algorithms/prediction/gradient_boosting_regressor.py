from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterMapLayer,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISGradientBoostingRegressor(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "gradient_boosting_regressor_train"
        self._display_name = "Gradient boosting regressor"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = "Train a gradient boosting regressor model"

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "target_labels",
            "validation_method",
            "validation_metric",
            "split_size",
            "cv_folds",
            "loss",
            "learning_rate",
            "n_estimators",
            "max_depth",
            "subsample",
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
            QgsProcessingParameterEnum(
                name=self.alg_parameters[6],
                description="Loss",
                options=["squared_error", "absolute_error", "huber", "quantile"],
                defaultValue="squared_error"
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[7],
                description="Learning rate",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.1,
                minValue=0.0001
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[8],
                description="N estimators",
                defaultValue=100,
                minValue=1
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[9],
                description="Max depth",
                optional=True,
                defaultValue=3,
                minValue=1
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[10],
                description="Subsample",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=1.0,
                minValue=0.0001,
                maxValue=1.0
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[11],
                description="Verbose",
                defaultValue=0,
                minValue=0,
                maxValue=2
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.alg_parameters[12],
                description="Random state",
                optional=True,
                minValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.alg_parameters[13],
                description="Output model",
                fileFilter='.joblib (*.joblib)'
            )
        )
