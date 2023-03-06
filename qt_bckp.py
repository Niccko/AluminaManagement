from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
from random import randint

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)



        self.graphWidget.setBackground('w')

        styles = {"color": "#000", "font-size": "15px"}
        self.graphWidget.setLabel("left", "Alumina quantity", **styles)
        self.graphWidget.setLabel("bottom", "Time", **styles)

        self.graphWidget.showGrid(x=True, y=True)

        bounds = self.g.get_bounds()

        self.graphWidget.setXRange(bounds[0][0], bounds[0][1] + 1, padding=0)
        self.graphWidget.setYRange(0, bounds[1][1], padding=0)

        self.pen = pg.mkPen(color=(255, 0, 0))
        self.graphWidget.plot(*self.g.get_data(),  pen=self.pen)
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)

        self.timer.timeout.connect(lambda: print("DSFSDF"))
        
        self.timer.start(100)

    def update_data(self):
        bounds = self.g.get_bounds()
        self.g.add_rate_point(bounds[0][1]+1, randint(0,4))
        self.graphWidget.setXRange(bounds[0][0], bounds[0][1] + 2, padding=0)
        self.graphWidget.setYRange(bounds[1][0], bounds[1][1], padding=0)
        self.update()
        
        self.graphWidget.plot(self.g.get_data()[0], self.g.get_data()[1],  pen=self.pen)
            

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
