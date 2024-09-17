import time
from typing import Any, Dict

import processing
from qgis.core import QgsProcessingFeedback
from qgis.PyQt.QtCore import QObject, QThread, pyqtSignal
from qgis.utils import iface

from eis_qgis_plugin.utils.model_feedback import EISProcessingFeedback


class AlgorithmExecutor(QObject):
    finished = pyqtSignal(dict, float)
    terminated = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

        self.worker = None
        self.worker_thread = None
        self.is_running = False
        self.is_terminated = False

        self.alg_name = None
        self.feedback = None


    def _cleanup(self):
        if self.worker:
            self.worker.deleteLater()
            self.worker = None
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.worker_thread.deleteLater()
            self.worker_thread = None
        self.is_running = False
        self.is_terminated = False


    def cancel(self):
        self.is_terminated = True
        if self.is_running:
            self.is_running = False
            if self.feedback:
                self.feedback.cancel()
            if self.worker_thread and self.worker_thread.isRunning():
                self.worker_thread.quit()
                self.worker_thread.wait()


    def on_finished(self, result):
        end = time.perf_counter()
        execution_time = end - self.start_time
        if self.is_terminated:
            self.terminated.emit()
        else:
            self.finished.emit(result, execution_time)
        self._cleanup()


    def on_error(self, error_message):
        iface.messageBar().pushWarning("Error: ", error_message)
        self.error.emit(error_message)
        self._cleanup()

    
    def update_feedback_progress(self, progress: int):
        self.feedback.progress_bar.setValue(progress)


    def update_feedback_text(self, text: str):
        self.feedback.text_edit.append(text)


    def configure(self, alg_name: str, feedback: EISProcessingFeedback):
        self.alg_name = alg_name
        if feedback is not self.feedback:
            self.feedback = feedback
            self.feedback.progress_signal.connect(self.update_feedback_progress)
            if self.feedback.text_edit is not None:
                self.feedback.text_signal.connect(self.update_feedback_text)


    def run(self, alg_parameters: Dict[str, Any]):
        if self.is_running:
            return
        
        self._cleanup()
        self.is_running = True
        self.start_time = time.perf_counter()

        self.worker = AlgorithmWorker(self.alg_name, alg_parameters, self.feedback)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)

        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

        self.feedback.setProgress(0)
        self.worker_thread.start()



class AlgorithmWorker(QObject):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, alg_name: str, params: Dict[str, Any], feedback: QgsProcessingFeedback) -> None:
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
