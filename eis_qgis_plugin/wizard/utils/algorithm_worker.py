import processing
from qgis.PyQt.QtCore import QObject, pyqtSignal


class AlgorithmWorker(QObject):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, alg_name, params, feedback):
        super().__init__()
        self.alg_name = alg_name
        self.params = params
        self.feedback = feedback

    def run(self):
        try:
            result = processing.run(
                self.alg_name,
                self.params,
                feedback=self.feedback
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
