from qgis.core import QgsMapLayer, QgsStyle, QgsVectorLayer
from qgis.gui import (
    QgsColorButton,
    QgsColorRampButton,
    QgsFieldComboBox,
    QgsMapLayerComboBox,
    QgsOpacityWidget,
)
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QFormLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from eis_qgis_plugin import pyqtgraph as pg
from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

from ..eda.plot_utils import generate_color_mapping, opacity_to_alpha

FORM_CLASS: QWidget = load_ui("explore/parallel_chart_tab.ui")


class ParallelChart(QWidget, FORM_CLASS):
    plot_container_parallel: QWidget

    layer_selection_parallel: QgsMapLayerComboBox
    color_field_selection_parallel: QgsFieldComboBox
    color_selection_parallel: QgsColorButton
    line_type_selection_parallel: QComboBox
    line_opacity_parallel: QgsOpacityWidget

    plot_button_parallel: QPushButton
    plot_button_parallel_plotly: QPushButton
    plot_button_seaborn: QPushButton
    clear_button_parallel: QPushButton
    clear_seaborn: QPushButton

    plot_style_form: QFormLayout

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_parallel_plotting()

        # Connect signals
        self.layer_selection_parallel.layerChanged.connect(self.update)
        self.plot_button_parallel.clicked.connect(self.plot_parallel_coordinates)
        self.plot_button_parallel_plotly.clicked.connect(
            self.plot_parallel_coordinates_plotly
        )
        self.plot_button_seaborn.clicked.connect(self.open_seaborn_graph)
        self.clear_button_parallel.clicked.connect(self.clear)
        self.clear_seaborn.clicked.connect(self.clear_fig)

        self.update(self.layer_selection_parallel.currentLayer())

    def init_parallel_plotting(self):
        # window = pg.GraphicsLayoutWidget()
        # self.plot_widget_parallel = win.addPlot()

        # # Assuming you have a list of your variable names
        # variable_names = ["var1", "var2", "var3"]

        # axis_items = []
        # for i, var in enumerate(variable_names):
        #     # create an AxisItem for this variable
        #     axis = AxisItem("left")
        #     # set the label of the AxisItem
        #     axis.setLabel(var)
        #     # Create a plot with axis
        #     plot_item = window.addPlot(axisItems={'left': axis})
        #     # add the AxisItem to the plot
        #     axis.linkToView(plot_item.vb)
        #     axis_items.append(axis)

        # # Assuming you have some data for your variables
        # data = [[1, 2, 3], [2, 3, 1], [3, 1, 2]]

        # for i, d in enumerate(data):
        #     # create a plot for this data, linked to the corresponding AxisItem
        #     plot_item.plot(d, pen=(i, len(data)))

        self.plot_widget_parallel = pg.PlotWidget(parent=self.plot_container_parallel)
        self.plot_widget_parallel.setMinimumSize(450, 430)
        self.plot_widget_parallel.setBackground("w")
        self.plot_widget_parallel.setTitle("Parallel coordinates plot")
        self.styles = {"color": "r", "font-size": "14px"}
        self.plot_widget_parallel.setLabel("left", "Y label", **self.styles)
        self.plot_widget_parallel.setLabel("bottom", "X label", **self.styles)

        self.plot_layout_parallel = QVBoxLayout(self.plot_container_parallel)
        self.plot_layout_parallel.addWidget(self.plot_widget_parallel)

        # Add color ramp widget (it is not available in Qt Designer)
        self.color_ramp_button = QgsColorRampButton()
        self.plot_style_form.insertRow(1, "Color ramp", self.color_ramp_button)

        # Get the default style manager
        style_manager = QgsStyle.defaultStyle()

        # Get a predefined color ramp by its name
        spectral_color_ramp = style_manager.colorRamp("Spectral")

        self.color_ramp_button.setDefaultColorRamp(spectral_color_ramp)
        self.color_ramp_button.setColorRamp(spectral_color_ramp)

    def update(self, layer: QgsMapLayer) -> None:
        if layer is not None:
            self.color_field_selection_parallel.setLayer(layer)

    def clear(self):
        self.plot_widget_parallel.clear()

    @staticmethod
    def normalize_value(layer: QgsVectorLayer, value: float, i: int):
        data_min = float(layer.minimumValue(i))
        data_max = float(layer.maximumValue(i))
        if data_max != data_min:  # to prevent division by zero
            normalized_value = (value - data_min) / (data_max - data_min)
        else:
            normalized_value = 0
        return normalized_value

    def plot_parallel_coordinates(self):
        layer = self.layer_selection_parallel.currentLayer()
        if not layer:
            print("No layer selected")
            return

        color_field_name = self.color_field_selection_parallel.currentField()
        if not color_field_name:
            print("No category field selected")
            return

        fields = layer.fields()
        alpha = opacity_to_alpha(self.line_opacity_parallel.opacity())
        color_mapping = generate_color_mapping(
            layer, color_field_name, self.color_ramp_button.colorRamp()
        )
        numerical_field_names = [
            field.name() for field in fields if field.name() != color_field_name
        ]
        data_x = list(range(len(numerical_field_names)))
        field_labels = zip(data_x, numerical_field_names)

        for feature in layer.getFeatures():
            # Determine feature color
            color_field_value = feature[color_field_name]
            pen_color = color_mapping[color_field_value]
            pen = pg.mkPen(
                pen_color.red(), pen_color.green(), pen_color.blue(), alpha, width=3
            )

            # Collect data
            data_y = []
            for i, field in enumerate(fields):
                field_name = field.name()
                if field_name in numerical_field_names:
                    value = float(feature[field_name])
                    normalized_value = self.normalize_value(layer, value, i)
                    data_y.append(normalized_value)

            self.plot_widget_parallel.plot(
                data_x, data_y, pen=pen, name=str(value), labels=field_labels
            )

        # Rename axis labels
        bottom_axis = self.plot_widget_parallel.getAxis("bottom")
        # print(numerical_field_names)
        bottom_axis.setTicks([field_labels])


    def open_seaborn_graph(self):
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.figure import Figure
        from PyQt5.QtWidgets import QDialog, QVBoxLayout

        from eis_qgis_plugin.libs.seaborn import barplot

        # self.plot_dialog = QDialog()

        # layout = QVBoxLayout()
        # self.plot_dialog.setLayout(layout)

        # pixmap = QtGui.QPixmap("/home/niko/Downloads/sns_out.svg")
        # label = QLabel()
        # label.setPixmap(pixmap)

        # layout.addWidget(label)
        # self.plot_dialog.show()

        # In your main application / widget, you would then create and show the dialog:
        dialog = QDialog()
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)

        # Create a Seaborn plot
        ax = self.fig.add_subplot(111)
        barplot(x=[1, 2, 3, 4], y=[1, 2, 3, 4], ax=ax)

        # Add the Matplotlib canvas to the dialog
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        dialog.setLayout(layout)
        self.canvas.draw()

        dialog.show()
        dialog.exec()

    def clear_fig(self):
        self.fig.clear()
        self.canvas.draw()
