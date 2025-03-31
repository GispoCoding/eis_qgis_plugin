from qgis.core import QgsProcessingFeedback
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QProgressBar, QTextEdit


class EISProcessingFeedback(QgsProcessingFeedback):

    PROGRESS_PREFIX = "Progress:"  # Should be same as in EISToolkitInvoker
    ERROR_PREFIX = "ValueError:"

    text_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)

    def __init__(self, text_edit: QTextEdit = None, progress_bar: QProgressBar = None):
        super().__init__()
        self.no_errors = True
        self.text_edit = text_edit
        self.progress_bar = progress_bar

    def setProgress(self, progress: int):
        if self.progress_bar is not None:
            self.progress_signal.emit(progress)

    def pushInfo(self, info):
        if self.text_edit is not None:
            if self.PROGRESS_PREFIX in info:
                progress = int(info.split(":")[1].strip()[:-1])
                self.setProgress(progress)
                self.text_signal.emit(f"Progress: {progress}%")
            elif self.ERROR_PREFIX in info:
                self.reportError(info)
            else:
                self.text_signal.emit(info)

    def pushCommandInfo(self, info):
        if self.text_edit is not None:
            self.text_signal.emit(f"Command: {info}")

    def pushDebugInfo(self, info):
        if self.text_edit is not None:
            self.text_signal.emit(f"Debug: {info}")

    def pushConsoleInfo(self, info):
        if self.text_edit is not None:
            self.text_signal.emit(f"Console: {info}")

    def reportError(self, error, fatalError=False):
        if self.text_edit is not None:
            self.no_errors = False
            self.text_signal.emit(f"Error: {error}")

    def report_terminated_execution(self, msg = ""):
        if self.text_edit is not None:
            self.text_signal.emit(str(msg))

    def report_failed_run(self):
        if self.text_edit is not None:
            self.text_signal.emit("Model training failed, not saving to history")
