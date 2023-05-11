from PyQt5.QtWidgets import QDialog
from qgis.gui import QgisInterface
from qgis.PyQt import QtCore, QtWidgets

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QDialog = load_ui("wizard_preprocess_window2.ui")


class EISWizardPreprocess(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, iface: QgisInterface) -> None:
        super().__init__()
        self.setupUi(self)
        self.iface = iface

        # self.create_scroll_area()

    # def create_scroll_area(self):
    #     page = self.geoprocessing_3

    #     h_layout = QtWidgets.QHBoxLayout()
    #     scroll = QtWidgets.QScrollArea(page)
    #     scroll.setWidgetResizable(True) # CRITICAL

    #     inner = QtWidgets.QFrame(scroll)
    #     inner.setGeometry(QtCore.QRect(460, 80, 500, 500))

    #     layout = QtWidgets.QVBoxLayout()

    #     inner.setLayout(layout)
    #     scroll.setWidget(inner) # CRITICAL
    #     h_layout.addWidget(scroll)

    #     for i in range(10):

    #         # b = QtWidgets.QPushButton(inner)
    #         # b.setText(str(i))

    #         # b = self.create_group_box(i)

    #         b = QtWidgets.QGroupBox(inner)
    #         b.setTitle(f"AAA {i}")

    #         c = QtWidgets.QPushButton(b)
    #         c.setText(str(i))
    #         inner.layout().addWidget(b)

    # def create_group_box(self, i):
    #     groupBox = QtWidgets.QGroupBox()
    #     groupBox.setFlat(False)
    #     groupBox.setObjectName(f"group_box{i}")
    #     label = QtWidgets.QLabel(groupBox)
    #     label.setGeometry(QtCore.QRect(10, 30, 441, 81))
    #     label.setStyleSheet("font: italic 11pt \"Ubuntu\";")
    #     label.setWordWrap(True)
    #     label.setObjectName(f"label{i}")
    #     label.setText("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque ullamcorper suscipit tortor, ac sagittis nibh cursus vel. Pellentesque nec sem nec lectus vulputate sodales ut in odio. Nullam nec tincidunt diam, vitae finibus purus. Sed rutrum malesuada odio, in imperdiet tortor commodo eu.")
    #     pushButton = QtWidgets.QPushButton(groupBox)
    #     pushButton.setGeometry(QtCore.QRect(460, 80, 89, 25))
    #     pushButton.setObjectName(f"pushButton{i}")

    #     return groupBox
