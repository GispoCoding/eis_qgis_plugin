from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterMapLayer,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISLogisticRegression(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "logistic_regression_train"
        self._display_name = "Logistic regression"
        self._group = "Prediction"
        self._group_id = "prediction"
        self._short_help_string = """
            Train and optionally validate a Logistic Regression classifier model using Sklearn.

            Various options and configurations for model performance evaluation are available. No validation, \
            split to train and validation parts, and cross-validation can be chosen. If validation is performed, \
            metric(s) to calculate can be defined and validation process configured (cross-validation method, \
            number of folds, size of the split). Depending on the details of the validation process, \
            the output metrics dictionary can be empty, one-dimensional or nested.

            The choice of the algorithm depends on the penalty chosen. Supported penalties by solver: \
            'lbfgs' - ['l2', None] \
            'liblinear' - ['l1', 'l2'] \
            'newton-cg' - ['l2', None] \
            'newton-cholesky' - ['l2', None] \
            'sag' - ['l2', None] \
            'saga' - ['elasticnet', 'l1', 'l2', None]

            For more information about Sklearn Logistic Regression, read the documentation here: \
            https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_rasters",
            "target_labels",
            "validation_method",
            "validation_metrics",
            "split_size",
            "cv_folds",
            "penalty",
            "max_iter",
            "solver",
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
            options=["accuracy", "precision", "recall", "f1", "auc"],
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

        penalty_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[6],
            description="Penalty",
            options=["l2", "l1", "elasicnet"],
            defaultValue=0,
            optional=True
        )
        penalty_param.setHelp("Specifies the norm of the penalty.")
        self.addParameter(penalty_param)

        max_iter_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[7],
            description="Max iter",
            defaultValue=100,
            minValue=1
        )
        max_iter_param.setHelp("Maximum number of iterations taken for the solvers to converge.")
        self.addParameter(max_iter_param)

        solver_param = QgsProcessingParameterEnum(
            name=self.alg_parameters[8],
            description="Solver",
            options=["lbfgs", "liblinear", "newton-cg", "newton-cholesky", "sag", "saga"],
            defaultValue=0
        )
        solver_param.setHelp("Algorithm to use in the optimization problem.")
        self.addParameter(solver_param)

        verbose_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[9],
            description="Verbose",
            defaultValue=0,
            minValue=0,
            maxValue=2
        )
        verbose_param.setHelp(
            "Specifies if modeling progress and performance should be printed. 0 doesn't print, \
            values 1 or above will produce prints."
        )
        self.addParameter(verbose_param)

        random_state_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[10],
            description="Random state",
            optional=True,
            minValue=0
        )
        random_state_param.setHelp("Seed for random number generation.")
        self.addParameter(random_state_param)

        output_model_param = QgsProcessingParameterFileDestination(
            name=self.alg_parameters[11],
            description="Output model",
            fileFilter='.joblib (*.joblib)'
        )
        output_model_param.setHelp("The trained model saved to file.")
        self.addParameter(output_model_param)
