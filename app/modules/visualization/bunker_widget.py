from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtWidgets, QtGui
from modules.visualization.utils import draw_rect_bottom
from utils.events.event_bus import EventBus


class BunkerWidget(QtWidgets.QWidget):
    def __init__(self, container) -> None:
        self.bars_width = 2541
        self.bunker_margin = 5
        self.bunker_offset = 40
        self.correct_offset = 0
        self.bunker_width = 0
        self.bar_height = 340
        self.selectedBunker = None

        self.container = container
        self.canvas = QtGui.QPixmap(self.bars_width, 391)
        self.canvas.fill(Qt.white)
        self.container.setPixmap(self.canvas)

        self.container.mousePressEvent = self.get_clicked_bunker_id

        self.painter = QtGui.QPainter(self.container.pixmap())
        self.pen = QtGui.QPen()
        self.brush = QtGui.QBrush()
        self.brush.setStyle(Qt.Dense1Pattern)
        self.painter.setPen(self.pen)
        self.painter.setBrush(self.brush)

        EventBus.add_event("selectedBunkerChanged")
        

    def paintEvent(self, bunker_data):
        QtGui.QPixmapCache.clear()
        self.container.pixmap().fill(Qt.white)
        bunker_count = len(bunker_data)
        # TODO Выглядит как *****, придумать как сразу их центровать---
        self.bunker_width = int((self.bars_width - 2*self.bunker_offset -
                           self.bunker_margin*(bunker_count-1))/bunker_count+1)
        self.correct_offset = int((self.bars_width - (self.bunker_width +
                             self.bunker_margin)*bunker_count - self.bunker_margin)/2)
        # -------------------------------------------------------------
        for i, bunker in enumerate(bunker_data):
            quantity = bunker[2]
            percentage = quantity / bunker[1] if quantity else 0
            color = QtGui.QColor(int(255*(1-percentage)),
                                 int(255*percentage), 0)
            if i+1 == self.selectedBunker:
                color.setAlpha(120)
            normalized_qnt = percentage * self.bar_height

            self.brush.setColor(color)
            self.painter.setBrush(self.brush)
            draw_rect_bottom(
                self.painter,
                self.correct_offset+i*(self.bunker_width+self.bunker_margin),
                380,
                self.bunker_width,
                int(normalized_qnt)
            )

    def get_clicked_bunker_id(self, event):
        x = event.pos().x() - self.correct_offset
        self.selectedBunker = int(x/(self.bunker_width+self.bunker_margin))+1
        EventBus.invoke("selectedBunkerChanged", bunker_id = self.selectedBunker)


