from qgis.core import QgsProcessingFeedback
from qgis.PyQt.QtWidgets import QProgressBar, QTextEdit


class EISModelGUIFeedback(QgsProcessingFeedback):

    PROGRESS_PREFIX = "Progress:"  # Should be same as in EISToolkitInvoker
    ERROR_PREFIX = "ValueError:"

    def __init__(self, text_edit: QTextEdit, progress_bar: QProgressBar = None):
        super().__init__()
        self.no_errors = True
        self.text_edit = text_edit
        self.progress_bar = progress_bar

    def setProgress(self, progress: int):
        if self.progress_bar is not None:
            self.progress_bar.setValue(progress)

    def pushInfo(self, info):
        if self.PROGRESS_PREFIX in info:
            progress = int(info.split(":")[1].strip()[:-1])
            self.setProgress(progress)
            self.text_edit.append(f"Progress: {progress}%")
        elif self.ERROR_PREFIX in info:
            self.reportError(info)
        else:
            self.text_edit.append(info)

    def pushCommandInfo(self, info):
        self.text_edit.append(f"Command: {info}")

    def pushDebugInfo(self, info):
        self.text_edit.append(f"Debug: {info}")

    def pushConsoleInfo(self, info):
        self.text_edit.append(f"Console: {info}")

    def reportError(self, error, fatalError=False):
        self.no_errors = False
        self.text_edit.append(f"Error: {error}")

    def report_failed_run(self):
        self.text_edit.append("Model training failed, not saving to database")
