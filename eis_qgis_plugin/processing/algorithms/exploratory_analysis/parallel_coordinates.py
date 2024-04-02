from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISParallelCoordinates(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "parallel_coordinates"
        self._display_name = "Plot parallel coordinates"
        self._group = "Exploratory analysis"
        self._group_id = "exploratory_analysis"
        self._short_help_string = """
            Generate a parallel coordinates plot for vector data.
            
            Automatically removes all rows containing null/nan values. \
            If more than 8 columns are present (after numeric filtering), keeps only the first 8 to plot.
        """

    def initAlgorithm(self, config=None):

        self.alg_parameters = [
            "input_vector",
            "color_column_name",
            "plot_title",
            "palette_name",
            "curved_lines",
            "show_plot",
            "save_dpi",
            "output_file"
        ]

        input_vector_param = QgsProcessingParameterFeatureSource(
            name=self.alg_parameters[0], description="Input vector"
        )
        input_vector_param.setHelp("Input vector file with features to plot.")
        self.addParameter(input_vector_param)

        color_column_param = QgsProcessingParameterField(
            name=self.alg_parameters[1],
            description="Color column",
            parentLayerParameterName=self.alg_parameters[0],
        )
        color_column_param.setHelp("The column to use for color encoding.")
        self.addParameter(color_column_param)

        plot_title_parameter = QgsProcessingParameterString(
            name=self.alg_parameters[2],
            description="Plot title",
            optional=True
        )
        plot_title_parameter.setHelp("Title of the produced plot.")
        self.addParameter(plot_title_parameter)

        palette_name_param = QgsProcessingParameterString(
            name=self.alg_parameters[3], description="Palette name", optional=True
        )
        palette_name_param.setHelp(
            "Palette to use for coloring. Should be a palette name accepted by Seaborn. " +
            "If not defined, default to viridis for continuous color column and spectral for " +
            "categorical color column."
        )
        self.addParameter(palette_name_param)

        curved_lines_param = QgsProcessingParameterBoolean(
            name=self.alg_parameters[4], description="Curved lines", defaultValue=True
        )
        curved_lines_param.setHelp("Whether the produced lines in the plot should be curvy or straight.")
        self.addParameter(curved_lines_param)

        show_plot_param = QgsProcessingParameterBoolean(
            name=self.alg_parameters[5], description="Show plot immediately"
        )
        show_plot_param.setHelp(
            "If the produced plot should be displayed immediately. Note that the algorithm " +
            "does not finish before the popup window is closed."
        )
        self.addParameter(show_plot_param)

        save_dpi_param = QgsProcessingParameterNumber(
            name=self.alg_parameters[6],
            description="Save dpi",
            optional=True,
            minValue=1
        )
        save_dpi_param.setHelp(
            "Controls the resolution of the plot. Higher values will lead to more detailed plots. " +
            "If not set, the underlying plot library determines the output dpi."
        )
        self.addParameter(save_dpi_param)

        output_file_param = QgsProcessingParameterFileDestination(
            name=self.alg_parameters[7],
            description="Output file",
            fileFilter='PNG files (*.png);;JPEG files (*.jpg *.jpeg);;PDF files (*.pdf);;SVG files (*.svg)'
        )
        output_file_param.setHelp("The output plot file.")
        self.addParameter(output_file_param)
