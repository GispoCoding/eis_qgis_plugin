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
        self._short_help_string = """
            Train and optionally validate a Gradient Boosting regressor model using Sklearn.

            Various options and configurations for model performance evaluation are available. No validation, \
            split to train and validation parts, and cross-validation can be chosen. If validation is performed, \
            metric(s) to calculate can be defined and validation process configured (cross-validation method, \
            number of folds, size of the split). Depending on the details of the validation process, \
            the output metrics dictionary can be empty, one-dimensional or nested.

            For more information about Sklearn Gradient Boosting regressor read the documentation here: \
            https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "target_labels",
            "validation_method",
            "validation_metrics",
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

        evidence_data_param = QgsProcessingParameterMultipleLayers(
            name=self.alg_parameters[0], description="Evidence data", layerType=QgsProcessing.TypeRaster
        )
        evidence_data_param.setHelp("Evidence rasters used for training.")
        self.addParameter(evidence_data_param)

        target_labels_param = QgsProcessingParameterMapLayer(
            name=self.alg_parameters[1], description="Target labels"
        )
        target_labels_param.setHelp("Target labels used for training.")
        self.addParameter(target_labels_param)

        validation_method_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[2],
            description="Validation method",
            options=["split", "kfold_cv", "skfold_cv", "loo_cv", "none"],
            defaultValue=0
        )
        validation_method_param.setHelp(
            "Validation method to use. 'split' divides data into two parts, 'kfold_cv' \
            performs k-fold cross-validation, 'skfold_cv' performs stratified k-fold cross-validation, \
            'loo_cv' performs leave-one-out cross-validation and 'none' will not validate model at all \
            (in this case, all X and y will be used solely for training)."
        )
        self.addParameter(validation_method_param)

        validation_metrics_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[3],
            description="Validation metrics",
            options=["mse", "rmse", "mae", "r2"],
            defaultValue=0,
            allowMultiple=True
        )
        validation_metrics_param.setHelp("Metrics to use for scoring the model if a validation method is selected.")
        self.addParameter(validation_metrics_param)

        split_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[4],
            description="Split size",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=0.2,
            minValue=0.001,
            maxValue=0.999
        )
        split_size_param.setHelp(
            "Fraction of the dataset to be used as validation data (rest is used for training). \
            Used only when validation_method is 'split'."
        )
        self.addParameter(split_size_param)

        cv_folds_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[5],
            description="CV folds",
            defaultValue=5,
            minValue=2
        )
        cv_folds_param.setHelp(
            "Number of folds used in cross-validation. Used only when validation_method is 'kfold_cv' \
            or 'skfold_cv'."
        )
        self.addParameter(cv_folds_param)

        loss_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[6],
            description="Loss",
            options=["squared_error", "absolute_error", "huber", "quantile"],
            defaultValue=0
        )
        loss_param.setHelp("The loss function to be optimized.")
        self.addParameter(loss_param)

        learning_rate_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[7],
            description="Learning rate",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=0.1,
            minValue=0.0001
        )
        learning_rate_param.setHelp("Shrinks the contribution of each tree.")
        self.addParameter(learning_rate_param)

        n_estimators_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[8],
            description="N estimators",
            defaultValue=100,
            minValue=1
        )
        n_estimators_param.setHelp(
            "The number of boosting stages to run. Gradient boosting is fairly robust to over-fitting \
            so a large number can result in better performance."
        )
        self.addParameter(n_estimators_param)

        max_depth_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[9],
            description="Max depth",
            optional=True,
            defaultValue=3,
            minValue=1
        )
        max_depth_param.setHelp(
            "Maximum depth of the individual regression estimators. The maximum depth limits the number \
            of nodes in the tree. Values must be >= 1 or None, in which case nodes are expanded until all leaves \
            are pure or until all leaves contain less than min_samples_split samples."
        )
        self.addParameter(max_depth_param)

        subsample_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[10],
            description="Subsample",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=1.0,
            minValue=0.0001,
            maxValue=1.0
        )
        subsample_param.setHelp(
            "The fraction of samples to be used for fitting the individual base learners. \
            If smaller than 1.0 this results in Stochastic Gradient Boosting. Subsample interacts with the \
            parameter n_estimators. Choosing subsample < 1.0 leads to a reduction of variance and an increase in bias."
        )
        self.addParameter(subsample_param)

        verbose_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[11],
            description="Verbose",
            defaultValue=0,
            minValue=0,
            maxValue=2
        )
        verbose_param.setHelp(
            "Specifies if modeling progress and performance should be printed. 0 doesn't print, \
            1 prints once in a while depending on the number of tress, 2 or above will print for every tree."
        )
        self.addParameter(verbose_param)

        random_state_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[12],
            description="Random state",
            optional=True,
            minValue=0
        )
        random_state_param.setHelp("Seed for random number generation.")
        self.addParameter(random_state_param)

        output_model_param = QgsProcessingParameterFileDestination(
            name=self.alg_parameters[13],
            description="Output model",
            fileFilter='.joblib (*.joblib)'
        )
        output_model_param.setHelp("The trained model saved to file.")
        self.addParameter(output_model_param)
