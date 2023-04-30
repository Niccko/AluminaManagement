from PyQt5 import QtWidgets
import pyqtgraph as pg
from modules import bunker_manager
import modules.configuration as config
from datetime import datetime


class QuantityGraph(QtWidgets.QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(QuantityGraph, self).__init__(*args, **kwargs)
        self.setParent(parent)
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setParent(self)
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setFixedSize(parent.size())

    def generate_tick(self, k: datetime):
        pass

    def draw(self, bunker_id):
        show_window = int(config.get("qnt_show_window"))
        bunker = bunker_manager.get_bunker(bunker_id)
        if not bunker:
            return
        include_est = 0 if bunker.is_aas else 2
        qnt_states = bunker_manager.get_quantity_info(bunker_id, show_window, include_est=include_est)
        times = [x.measure_dt.timestamp() - datetime.now().timestamp() for x in qnt_states]
        values = [x.quantity for x in qnt_states]
        self.graphWidget.setXRange(times[-1], times[-1] + show_window + 30)
        self.graphWidget.plot(times, values, symbol="o", symbolPen='b')

    def draw_prediction(self, bunker_id, remaining_time):
        bunker = bunker_manager.get_bunker(bunker_id)
        if not bunker:
            return
        include_est = 0 if bunker.is_aas else 2
        qnt_state = bunker_manager.get_quantity_info(bunker_id, 1, include_est=include_est)
        if not qnt_state:
            return
        qnt_state_dt = float(datetime.timestamp(qnt_state[0].measure_dt))
        pen = pg.mkPen(color=(255, 0, 0))

        self.graphWidget.plot(
            [qnt_state_dt - datetime.now().timestamp(), qnt_state_dt - datetime.now().timestamp() + remaining_time],
            [qnt_state[0].quantity, 0], pen=pen)
