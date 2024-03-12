from ..functions import mkPen
from ..Qt import QtCore, QtGui, QtWidgets


class PenPreviewLabel(QtWidgets.QLabel):
    def __init__(self, param):
        super().__init__()
        self.param = param
        self.pen = QtGui.QPen(self.param.pen)
        param.sigValueChanging.connect(self.onPenChanging)

    def onPenChanging(self, param, val):
        self.pen = QtGui.QPen(val)
        self.update()

    def paintEvent(self, ev):
        path = QtGui.QPainterPath()
        displaySize = self.size()
        w, h = displaySize.width(), displaySize.height()
        # draw a squiggle with the pen
        path.moveTo(w * 0.2, h * 0.2)
        path.lineTo(w * 0.4, h * 0.8)
        path.cubicTo(w * 0.5, h * 0.1, w * 0.7, h * 0.1, w * 0.8, h * 0.8)

        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.drawPath(path)

        # No indication of "cosmetic" from just the paint path, so add something extra in that case
        if self.pen.isCosmetic():
            painter.setPen(mkPen("k"))
            painter.drawText(QtCore.QPointF(w * 0.81, 12), "C")
        painter.end()
