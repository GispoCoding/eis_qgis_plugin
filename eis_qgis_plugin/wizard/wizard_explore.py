from PyQt5.QtWidgets import QDialog
from qgis.gui import QgisInterface
from qgis.PyQt import QtWidgets, QtCore
from qgis.PyQt.QtWebKitWidgets import QWebView
from qgis.PyQt.QtWebKit import QWebSettings

# from PyQt5.QtWebEngineWidgets import QWebEngineView

from eis_qgis_plugin.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS: QDialog = load_ui("wizard_explore_window2.ui")


class EISWizardExplore(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, iface: QgisInterface) -> None:
        super().__init__()
        self.setupUi(self)
        self.iface = iface

        # self.load_chart()
        # self.load_chart_web_engine()

    def load_chart(self):
        # html = "file:///home/niko/code/plugin_dev/eis_toolkit/eis_toolkit/bokeh_test.html"
        # html = "file:///home/niko/Downloads/testi.html"
        html = "file:///home/niko/Downloads/bokeh_test_embedded.html"
        self.web_view = QWebView(self)
        self.web_view.settings().setAttribute(QWebSettings.LocalContentCanAccessFileUrls, True)
        path = QtCore.QUrl(html)
        # path = QtCore.QUrl("https://github.com/GispoCoding/eis_toolkit")
        self.web_view.setUrl(path)
        # with open(html, 'r') as file:
        #     html_content = file.read()
        #     print(html_content)
        #     self.web_view.setHtml(html_content, QtCore.QUrl.fromLocalFile(html))
        #     self.web_view.show()

    # def load_chart_web_engine(self):
    #     html = "file:///home/niko/Downloads/bokeh_test_embedded.html"
    #     self.web_view = QWebEngineView()
    #     self.web_view.load(QtCore.QUrl.fromLocalFile(html))


class EISWizardExploreBig(QtWidgets.QDialog, load_ui("wizard_explore_big.ui")):
    def __init__(self, iface: QgisInterface) -> None:
        super().__init__()
        self.setupUi(self)
        self.iface = iface
