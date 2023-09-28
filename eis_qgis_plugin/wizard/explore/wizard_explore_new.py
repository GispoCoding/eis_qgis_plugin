from qgis.PyQt.QtWidgets import (
    QDialog,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QFrame,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QSizePolicy,
    QFormLayout,
    QListWidget,
    QLabel
)

from qgis.core import QgsMapLayer, NULL 

from qgis.PyQt.QtGui import QColor
from qgis import processing

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from qgis.utils import iface

from qgis.gui import (
    QgsMapLayerComboBox,
    QgsFieldComboBox,
    QgsColorButton,
    QgsOpacityWidget,
)

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui


FORM_CLASS: QDialog = load_ui("explore/wizard_explore_window_new.ui")


class EISWizardExploreNew(QDialog, FORM_CLASS):
    tab_widget: QTabWidget

    # Tabs
    data_summary_tab: QWidget
    univariate_analysis_tab: QWidget
    bivariate_analysis_tab: QWidget
    multivariate_analysis_tab: QWidget
    geospatial_analysis_tab: QWidget

    # Data summary tab contents
    data_summary_layer_selection: QgsMapLayerComboBox
    data_summary_field_selection: QgsFieldComboBox
    data_summary_band_selection: QComboBox
    compute_btn: QPushButton
    layer_properties_btn: QPushButton

    n_total: QLabel
    n_valid: QLabel
    n_null: QLabel
    mean: QLabel
    stdev: QLabel
    relative_stdev: QLabel
    variance: QLabel
    skewness: QLabel
    kurtosis: QLabel
    min: QLabel
    quantile25: QLabel
    median: QLabel
    quantile75: QLabel
    max: QLabel
    a_squared: QLabel
    p_value: QLabel

    # Univariate tab contents
    container: QWidget
    plot_customization_form: QFormLayout
    univariate_plot_container: QFrame
    layer_selection: QgsMapLayerComboBox
    fields_selection: QListWidget
    plot_type_selection: QComboBox
    # palette_selection: QgsColorRampButton
    color_selection: QgsColorButton
    opacity_selection: QgsOpacityWidget
    log_scale_selection: QComboBox
    fill_selection: QComboBox
    multiple_selection: QComboBox
    hist_stat_selection: QComboBox
    element_selection: QComboBox
    nr_of_bins_selection: QSpinBox
    bw_adjust_selection: QDoubleSpinBox
    ecdf_stat_selection: QComboBox

    plot_btn: QPushButton
    clear_btn: QPushButton
    reset_btn: QPushButton

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.initialize_summary_tab()
        self.initialize_univariate_tab()

        # self.palette_selection = QgsColorRampButton()
        # # Get the default style manager
        # style_manager = QgsStyle.defaultStyle()

        # # Get a predefined color ramp by its name
        # spectral_color_ramp = style_manager.colorRamp("Spectral")

        # self.palette_selection.setDefaultColorRamp(spectral_color_ramp)
        # self.palette_selection.setColorRamp(spectral_color_ramp)
        # self.plot_customization_form.insertRow(3, "Palette", self.palette_selection)

    def initialize_summary_tab(self):
        self.data_summary_layer_selection.layerChanged.connect(self.set_field_or_band)
        self.compute_btn.clicked.connect(self.compute_statistics)
        self.layer_properties_btn.clicked.connect(self.open_layer_properties)

        self.data_summary_field_selection.setLayer(self.data_summary_layer_selection.currentLayer())

    def initialize_univariate_tab(self):
        self.plot_btn.clicked.connect(self.plot)
        self.clear_btn.clicked.connect(self.clear_plot)
        self.reset_btn.clicked.connect(self.reset)

        self.layer_selection.layerChanged.connect(self.set_layer)
        self.plot_type_selection.currentTextChanged.connect(self.set_buttons)

        self.plot_layout = QVBoxLayout()
        self.univariate_plot_container.setLayout(self.plot_layout)

        self.set_buttons(self.plot_type_selection.currentText())

    def compute_statistics(self):
        # Get N
        layer = self.data_summary_layer_selection.currentLayer()
        if layer.type() == QgsMapLayer.VectorLayer:  # NOTE: Same snippet later, refactor at some point
            field = self.data_summary_field_selection.currentField()
            all_values = [feature.attribute(field) for feature in layer.getFeatures()]
            nr_of_all_values = len(all_values)
            nr_of_nulls = len([value for value in all_values if value == NULL])
            nr_of_valids = nr_of_all_values - nr_of_nulls

        elif layer.type() == QgsMapLayer.RasterLayer:  # NOTE: Same snippet later, refactor at some point
            data_provider = layer.dataProvider()
            width = layer.width()
            height = layer.height()
            band = int(self.data_summary_band_selection.currentIndex())

            data_block = data_provider.block(band, layer.extent(), width, height)
            nr_of_nulls = 0
            nr_of_valids = 0
            nr_of_all_values = width * height

            # Loop over all pixels
            for row in range(height):
                for col in range(width):
                    pixel_value = data_block.value(row, col)
                    if pixel_value == NULL:
                        nr_of_nulls += 1
                    else:
                        nr_of_valids += 1

        else:
            raise Exception("Not vector or raster")
        

        self.n_total.setText(str(nr_of_all_values))
        self.n_null.setText(str(nr_of_nulls))
        self.n_valid.setText(str(nr_of_valids))

        # Get descriptive statistics
        
        if layer.type() == QgsMapLayer.VectorLayer:
            descriptive_statistics_results = processing.run("eis:descriptive_statistics_vector",
                                                            
                {
                    'input_file': self.data_summary_layer_selection.currentLayer(),
                    'column': self.data_summary_field_selection.currentField()
                }
            )
        else:
            descriptive_statistics_results = processing.run("eis:descriptive_statistics_raster",
                                                            
                {
                    'input_file': self.data_summary_layer_selection.currentLayer(),
                }
            )

        self.min.setText(str(descriptive_statistics_results["min"]))
        self.quantile25.setText(str(descriptive_statistics_results["25%"]))
        self.median.setText(str(descriptive_statistics_results["50%"]))
        self.quantile75.setText(str(descriptive_statistics_results["75%"]))
        self.max.setText(str(descriptive_statistics_results["max"]))

        self.mean.setText(str(descriptive_statistics_results["mean"]))
        self.stdev.setText(str(descriptive_statistics_results["standard_deviation"]))
        self.relative_stdev.setText(str(descriptive_statistics_results["relative_standard_deviation"]))
        self.skewness.setText(str(descriptive_statistics_results["skew"]))

    def open_layer_properties(self):
        iface.showLayerProperties(self.data_summary_layer_selection.currentLayer())

    def set_field_or_band(self, layer):
        self.data_summary_field_selection.setLayer(layer)
        self.data_summary_band_selection.clear()
    
        if layer.type() == QgsMapLayer.RasterLayer:
            bands = [f"Band {i + 1}" for i in range(layer.bandCount())]
            self.data_summary_band_selection.addItems(bands)


    def set_layer(self, layer):
        self.fields_selection.clear()  # Clear existing items
        if layer is not None:
            if layer.type() == QgsMapLayer.VectorLayer:
                for field in layer.fields():
                    self.fields_selection.addItem(field.name())
            elif layer.type() == QgsMapLayer.RasterLayer:
                for i in range(layer.bandCount()):
                    self.fields_selection.addItem(f"Band {i + 1}")

    def set_buttons(self, plot_type: str):
        if plot_type.lower() == "histogram":
            self.fill_selection.setEnabled(True)
            self.multiple_selection.setEnabled(True)

            self.hist_stat_selection.setEnabled(True)
            self.element_selection.setEnabled(True)
            self.nr_of_bins_selection.setEnabled(True)

            self.bw_adjust_selection.setEnabled(False)

            self.ecdf_stat_selection.setEnabled(False)

        elif plot_type.lower() == "kde":
            self.fill_selection.setEnabled(True)
            self.multiple_selection.setEnabled(True)

            self.hist_stat_selection.setEnabled(False)
            self.element_selection.setEnabled(False)
            self.nr_of_bins_selection.setEnabled(False)

            self.bw_adjust_selection.setEnabled(True)

            self.ecdf_stat_selection.setEnabled(False)
        
        elif plot_type.lower() == "histogram + kde":
            self.fill_selection.setEnabled(True)
            self.multiple_selection.setEnabled(True)

            self.hist_stat_selection.setEnabled(True)
            self.element_selection.setEnabled(True)
            self.nr_of_bins_selection.setEnabled(True)

            self.bw_adjust_selection.setEnabled(True)

            self.ecdf_stat_selection.setEnabled(False)

        elif plot_type.lower() == "ecdf":
            self.fill_selection.setEnabled(False)
            self.multiple_selection.setEnabled(False)

            self.hist_stat_selection.setEnabled(False)
            self.element_selection.setEnabled(False)
            self.nr_of_bins_selection.setEnabled(False)

            self.bw_adjust_selection.setEnabled(False)

            self.ecdf_stat_selection.setEnabled(True)


    def clear_plot(self):
        for i in reversed(range(self.plot_layout.count())):
            widget = self.plot_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def reset(self):
        self.fields_selection.clearSelection()

        self.plot_type_selection.setCurrentIndex(0)
        self.opacity_selection.setOpacity(90)
        self.log_scale_selection.setCurrentIndex(0)
        self.fill_selection.setCurrentIndex(0)
        self.multiple_selection.setCurrentIndex(0)
        self.hist_stat_selection.setCurrentIndex(0)
        self.element_selection.setCurrentIndex(0)
        self.nr_of_bins_selection.setValue(0)
        self.bw_adjust_selection.setValue(1.00)

    def get_bool(self, str: str) -> bool:
        return str.lower() == "true" 
    
    def qcolor_to_mpl(self, qcolor: QColor):
        """Convert QColor to Matplotlib color"""
        return qcolor.redF(), qcolor.greenF(), qcolor.blueF(), qcolor.alphaF()
    
    def qgsColorRamp_to_list(self, qgsColorRamp, steps=10):
        """Convert QgsColorRamp to a list of Seaborn-friendly colors"""
        colors = []
        for i in range(steps + 1):
            ratio = i / steps
            qcolor = qgsColorRamp.color(ratio)
            colors.append((qcolor.redF(), qcolor.greenF(), qcolor.blueF(), qcolor.alphaF()))
        return colors


    def plot(self):
        self.clear_plot()

        layer = self.layer_selection.currentLayer()
        selected_items = self.fields_selection.selectedItems()
        selected_fields = [item.text() for item in selected_items]

        data_dict = {}

        # Loop through each field and append its data to long_form_data
        for field in selected_fields:
            if layer.type() == QgsMapLayer.VectorLayer:
                values = [feature.attribute(field) for feature in layer.getFeatures()]
                data = [value for value in values if value != NULL]
                data_dict[field] = data
            # Raster
            else:  
                data_provider = layer.dataProvider()
                width = layer.width()
                height = layer.height()
                band = int(field.split()[-1])

                data_block = data_provider.block(band, layer.extent(), width, height)
                data = []

                # Loop over all pixels
                for row in range(height):
                    for col in range(width):
                        pixel_value = data_block.value(row, col)
                        if pixel_value != NULL:
                            data.append(pixel_value)
            data_dict[field] = data

        fig, ax = plt.subplots()

        sns_common_kwargs = {
            "data": data_dict,
            "fill": self.get_bool(self.fill_selection.currentText()),
            "multiple": self.multiple_selection.currentText().split()[0].lower(),
            "log_scale": self.get_bool(self.log_scale_selection.currentText()),
            "alpha": self.opacity_selection.opacity(),
            "ax": ax
        }

        if self.plot_type_selection.currentText().lower() == "histogram":
            sns.histplot(
                **sns_common_kwargs,
                stat=self.hist_stat_selection.currentText().lower(),
                element=self.element_selection.currentText().lower(),
                bins=self.nr_of_bins_selection.value() if self.nr_of_bins_selection.value() > 0 else "auto",
                # palette=self.qgsColorRamp_to_list(self.palette_selection.colorRamp(), len(selected_fields)),
                # color=self.qcolor_to_mpl(self.color_selection.color())
            )  
        
        elif self.plot_type_selection.currentText().lower() == "kde":
            sns.kdeplot(
                **sns_common_kwargs,
                bw_adjust=self.bw_adjust_selection.value(),
                # palette=self.qgsColorRamp_to_list(self.palette_selection.colorRamp(), len(selected_fields)),
                # color=self.qcolor_to_mpl(self.color_selection.color())
            )

        elif self.plot_type_selection.currentText().lower() == "histogram + kde":
            sns.histplot(
                **sns_common_kwargs,
                stat=self.hist_stat_selection.currentText().lower(),
                element=self.element_selection.currentText().lower(),
                bins=self.nr_of_bins_selection.value() if self.nr_of_bins_selection.value() > 0 else "auto",
                kde=True,
                kde_kws={"bw_adjust": self.bw_adjust_selection.value()},
                # palette=self.qgsColorRamp_to_list(self.palette_selection.colorRamp(), len(selected_fields)),
                # color=self.qcolor_to_mpl(self.color_selection.color())
            )  

        elif self.plot_type_selection.currentText().lower() == "ecdf":
            sns_common_kwargs.pop("fill")
            sns_common_kwargs.pop("multiple")
            sns.ecdfplot(
                **sns_common_kwargs,
                stat=self.ecdf_stat_selection.currentText().lower(),
                # palette=self.qgsColorRamp_to_list(self.palette_selection.colorRamp(), len(selected_fields)),
                # color=self.qcolor_to_mpl(self.color_selection.color())
            )  

        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar = NavigationToolbar(canvas, self.univariate_plot_container)

        self.plot_layout.addWidget(toolbar)
        self.plot_layout.addWidget(canvas)
