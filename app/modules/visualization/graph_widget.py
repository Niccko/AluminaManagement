from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtGui
import pyqtgraph as pg

class QuantityGraph(QtWidgets.QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(QuantityGraph, self).__init__(*args, **kwargs)
        self.setParent(parent)
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setParent(self)
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setFixedSize(parent.size())
        
        