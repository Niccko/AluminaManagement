from PyQt5 import Qt


def draw_rect_bottom(painter, x, y, w, h):
    painter.drawRect(x, y - h, w, h)


def color_lerp(color_a: Qt.QColor, color_b: Qt.QColor, perc):
    r = int((color_b.red() - color_a.red()) * perc + color_a.red())
    g = int((color_b.green() - color_a.green()) * perc + color_a.green())
    b = int((color_b.blue() - color_a.blue()) * perc + color_a.blue())
    return Qt.QColor(r, g, b, 255)
