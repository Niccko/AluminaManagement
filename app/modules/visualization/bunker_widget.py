from PyQt5.QtCore import Qt
from PyQt5.Qt import QColor
from PyQt5 import QtWidgets, QtGui
from modules.visualization.utils import draw_rect_bottom
from utils.events.event_bus import EventBus
from math import ceil
from modules.visualization.utils import color_lerp
from modules.bunker_manager import get_bunkers


class RectBoundary:
    def __init__(self, x, y, w, h):
        self.pos = (x, y)
        self.size = (w, h)

    def point_in_area(self, x, y):
        return self.pos[0] <= x <= self.pos[0] + self.size[0] \
            and self.pos[1] - self.size[1] <= y <= self.pos[1]


class BunkerObject(RectBoundary):
    def __init__(self, bunker_id, x, y, w, h, capacity, quantity, selected):
        super().__init__(x, y, w, h)
        self.bunker_id = bunker_id
        self.capacity = capacity
        self.quantity = quantity
        self.selected = selected

    def draw(self, painter, brush, color):

        percentage = self.quantity / self.capacity if self.quantity else 0
        if not color:
            color = color_lerp(QColor(249, 118, 110), QColor(0, 191, 124), percentage)
        if self.selected:
            color.setAlpha(120)

        brush.setColor(color)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        draw_rect_bottom(
            painter,
            self.pos[0],
            self.pos[1],
            self.size[0],
            int(self.size[1] * percentage)
        )
        brush.setColor(Qt.transparent)
        painter.setBrush(brush)
        draw_rect_bottom(
            painter,
            self.pos[0],
            self.pos[1],
            self.size[0],
            int(self.size[1])
        )


class BunkerWidget(QtWidgets.QWidget):
    def __init__(self, container, row_count) -> None:
        super().__init__()
        self.bunkers_in_row = None
        self.row_count = row_count
        self.bunker_margin = 5
        self.row_margin = 10
        self.bunker_offset = 40
        self.correct_offset = 0
        self.bunker_width = 0
        self.bar_height = (container.height() - 50) / row_count
        self.selectedBunker = None

        self.bunkers = []

        self.container = container
        self.canvas = QtGui.QPixmap(self.container.size())
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

    def paintEvent(self, bunker_data, color=None):
        self.bunkers = []
        bunker_count = len(bunker_data)
        if bunker_count > 0:
            self.bunkers_in_row = ceil(bunker_count / self.row_count)
            work_width = self.canvas.width() - 2 * self.bunker_offset - (self.bunkers_in_row - 1) * self.bunker_margin
            self.bunker_width = int(work_width / self.bunkers_in_row)

        else:
            self.bunker_width = 0
            self.correct_offset = 0
        for i, bunker in enumerate(bunker_data):
            self.bunkers.append(BunkerObject(
                bunker[0],
                self.bunker_offset + (i % self.bunkers_in_row) * (self.bunker_width + self.bunker_margin),
                int(10 + (self.bar_height + self.row_margin) * ceil(i // self.bunkers_in_row + 1)),
                self.bunker_width,
                self.bar_height,
                bunker[1],
                bunker[2],
                bunker[0] == self.selectedBunker
            ))
        for i in self.bunkers:
            i.draw(self.painter, self.brush, color=color)

    def get_clicked_bunker_id(self, event):
        x = event.pos().x()
        y = event.pos().y()
        for b in self.bunkers:
            if b.point_in_area(x, y):
                self.selectedBunker = b.bunker_id
                EventBus.invoke("selectedBunkerChanged", bunker_id=self.selectedBunker)
