import re
from typing import Any, Dict, Optional

from qgis.core import (
    QgsProcessing,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterString,
)

from eis_qgis_plugin.eis_processing.eis_processing_algorithm import EISProcessingAlgorithm
from eis_qgis_plugin.eis_processing.eis_toolkit_invoker import EISToolkitInvoker


class EISCellBasedAssociation(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "cell_based_association"
        self._display_name = "Cell based association"
        self._group = "Vector processing"
        self._group_id = "vector_processing"
        self._short_help_string = """
            Create a CBA matrix.

            Cell-Based Association is used as a pre-processing method for geological data, such as \
            geological maps and structural data. This method allows identifying specific associations \
            of geological features across a given area (i.e. geological environments) using a regular \
            square grid. Associations of geological features are identified and synthetized into unique \
            binary codes, representing the absence or presence of each variable inside the environments.

            This method allows the analysis of point-environments relationship. Known occurences define \
            mineralized environments, which are used to compute favorability score, using various methods. \
            Such methods include Agglomerative Hierarchical Clustering (AHC), Ranking \
            (lithology/mineralization ratios) or Random Forest (RF) for instance.

            For more details about the CBA, see for instance: 

            **Tourlière, B., Pakyuz-Charrier, E., Cassard, D., Barbanson, L., & Gumiaux, C. (2015)**. \
            *Cell Based Associations: A procedure for considering scarce and mixed mineral occurrences in \
            predictive mapping*. Computers & geosciences, 78, 53-62.

            **A. Vella (2022)**. *Highlighting mineralized geological environments through a new Data-driven \
            predictive mapping approach*. PhD Thesis, University of Orléans, France.
        """

    def initAlgorithm(self, config=None):
        self.alg_parameters = [
            "input_vector",
            "cell_size",
            "column",
            "subset_target_attribute_values",
            "add_name",
            "add_buffer",
            "output_raster"
        ]

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0],
            description="Input vector",
            types=[QgsProcessing.TypeVectorPolygon, QgsProcessing.TypeVectorLine]
        )
        input_vector_param.setHelp("Input vector file.")
        self.addParameter(input_vector_param)

        cell_size_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[1],
            description="Cell size",
            minValue=0
        )
        cell_size_param.setHelp("Size of the cells in output raster.")
        self.addParameter(cell_size_param)

        column_param = QgsProcessingParameterField(
            name=self.alg_parameters[2],
            description="Column",
            parentLayerParameterName=self.alg_parameters[0],
            optional=True
        )
        column_param.setHelp(
            "Column of interest. If no attribute is specified, then an artificial attribute is \
            created representing the presence or absence of the geometries of this file for \
            each cell of the CBA grid. A categorical attribute will generate as many columns \
            (binary) in the CBA matrix than values considered of interest (dummification)."
        )
        self.addParameter(column_param)

        subset_target_attribute_values_param = QgsProcessingParameterString(
            name=self.alg_parameters[3],
            description="Subset target attributes",
            optional=True
        )
        subset_target_attribute_values_param.setHelp(
            "List of values of interest of the target attribute, in case a categorical target \
            attribute has been specified. Allows to filter a subset of relevant values. \
            Input the values as a comma-separated list. For example: value1, value2, value4, value8."
        )
        self.addParameter(subset_target_attribute_values_param)

        add_name_param = QgsProcessingParameterString(
            name=self.alg_parameters[4],
            description="Name",
            optional=True
        )
        add_name_param.setHelp("Name of the column to add to the matrix.")
        self.addParameter(add_name_param)

        add_buffer_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[5],
            description="Buffer",
            type=QgsProcessingParameterNumber.Double,
            optional=True
        )
        add_buffer_param.setHelp(
            "Allow the use of a buffer around shapes before the intersection with CBA cells for \
            the added vector features. Minimize border effects or allow increasing positive \
            samples (i.e. cells with mineralization). The size of the buffer is computed using the \
            CRS (if projected CRS in meters: value in meters)."
        )
        self.addParameter(add_buffer_param)

        output_raster_param = QgsProcessingParameterRasterDestination(
            name=self.alg_parameters[6], description="Output raster"
        )
        output_raster_param.setHelp("Output CBA raster.")
        self.addParameter(output_raster_param)


    def processAlgorithm(
        self,
        parameters: Dict[str, QgsProcessingParameterDefinition],
        context: QgsProcessingContext,
        feedback: Optional[QgsProcessingFeedback]
    ) -> Dict[str, Any]:
        if feedback is None:
            feedback = QgsProcessingFeedback()

        param_index = 3
        # Handle the value subset param
        values_raw = self.parameterAsString(parameters, self.alg_parameters[param_index], context)
        values = re.split(';|,', values_raw)
        values_options = []
        for value in values:
            values_options.append("--" + self.alg_parameters[param_index].replace("_", "-"))
            values_options.append(value) 

        # Remove breaks from the list to not prepare them again in the next step
        self.alg_parameters.pop(param_index)
        typer_args, typer_options, output_paths = self.prepare_arguments(parameters, context)
        typer_options += values_options  # Combine lists

        toolkit_invoker = EISToolkitInvoker()
        toolkit_invoker.assemble_cli_command(self.name(), typer_args, typer_options)
        results = toolkit_invoker.run_toolkit_command(feedback)

        self.get_results(results, parameters)
        for param_name, output_path in output_paths.items():
            results[param_name] = output_path

        feedback.setProgress(100)

        return results
