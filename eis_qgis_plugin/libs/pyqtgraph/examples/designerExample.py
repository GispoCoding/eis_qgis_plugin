"""
Simple example of loading UI template created with Qt Designer.

This example uses uic.loadUiType to parse and load the ui at runtime. It is also
possible to pre-compile the .ui file using pyuic (see VideoSpeedTest and
ScatterPlotSpeedTest examples; these .ui files have been compiled with the
tools/rebuildUi.py script).
"""

import os

import numpy as np
import pyqtgraph as pg

pg.mkQApp()

## Define main window class from template
path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, "designerExample.ui")
WindowTemplate, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class MainWindow(TemplateBaseClass):
    def __init__(self):
        TemplateBaseClass.__init__(self)
        self.setWindowTitle("pyqtgraph example: Qt Designer")

        # Create the main window
        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        self.ui.plotBtn.clicked.connect(self.plot)

        self.show()

    def plot(self):
        self.ui.plot.plot(np.random.normal(size=100), clear=True)


win = MainWindow()

if __name__ == "__main__":
    pg.exec()
