from qgis.PyQt.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from eis_qgis_plugin.wizard.eda.plotting import EISWizardPlotting


class EISWizardEDA(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.eda_tabs = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.eda_tabs)
        self.setLayout(layout)

        self.plot_page = EISWizardPlotting(self)
        self.eda_tabs.addTab(self.plot_page, "Plots")


    ## STATS

    # def compute_statistics(self):
    #     # Get N
    #     layer = self.data_summary_layer_selection.currentLayer()
    #     if (
    #         layer.type() == QgsMapLayer.VectorLayer
    #     ):  # NOTE: Same snippet later, refactor at some point
    #         field = self.data_summary_field_selection.currentField()
    #         all_values = [feature.attribute(field) for feature in layer.getFeatures()]
    #         nr_of_all_values = len(all_values)
    #         nr_of_nulls = len([value for value in all_values if value == NULL])
    #         nr_of_valids = nr_of_all_values - nr_of_nulls

    #     elif (
    #         layer.type() == QgsMapLayer.RasterLayer
    #     ):  # NOTE: Same snippet later, refactor at some point
    #         data_provider = layer.dataProvider()
    #         width = layer.width()
    #         height = layer.height()
    #         band = int(self.data_summary_band_selection.currentIndex())

    #         data_block = data_provider.block(band, layer.extent(), width, height)
    #         nr_of_nulls = 0
    #         nr_of_valids = 0
    #         nr_of_all_values = width * height

    #         # Loop over all pixels
    #         for row in range(height):
    #             for col in range(width):
    #                 pixel_value = data_block.value(row, col)
    #                 if pixel_value == NULL:
    #                     nr_of_nulls += 1
    #                 else:
    #                     nr_of_valids += 1

    #     else:
    #         raise Exception("Not vector or raster")

    #     self.n_total.setText(str(nr_of_all_values))
    #     self.n_null.setText(str(nr_of_nulls))
    #     self.n_valid.setText(str(nr_of_valids))

    #     # Get descriptive statistics

    #     if layer.type() == QgsMapLayer.VectorLayer:
    #         descriptive_statistics_results = processing.run(
    #             "eis:descriptive_statistics_vector",
    #             {
    #                 "input_file": self.data_summary_layer_selection.currentLayer(),
    #                 "column": self.data_summary_field_selection.currentField(),
    #             },
    #         )
    #     else:
    #         descriptive_statistics_results = processing.run(
    #             "eis:descriptive_statistics_raster",
    #             {
    #                 "input_file": self.data_summary_layer_selection.currentLayer(),
    #             },
    #         )

    #     self.min.setText(str(descriptive_statistics_results["min"]))
    #     self.quantile25.setText(str(descriptive_statistics_results["25%"]))
    #     self.median.setText(str(descriptive_statistics_results["50%"]))
    #     self.quantile75.setText(str(descriptive_statistics_results["75%"]))
    #     self.max.setText(str(descriptive_statistics_results["max"]))

    #     self.mean.setText(str(descriptive_statistics_results["mean"]))
    #     self.stdev.setText(str(descriptive_statistics_results["standard_deviation"]))
    #     self.relative_stdev.setText(
    #         str(descriptive_statistics_results["relative_standard_deviation"])
    #     )
    #     self.skewness.setText(str(descriptive_statistics_results["skew"]))
