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

    def draw(self, bunker_id):
        bunker = bunker_manager.get_bunker(bunker_id)
        if not bunker:
            return
        include_est = 0 if bunker.is_aas else 2
        qnt_states = bunker_manager.get_quantity_info(bunker_id, config.get("qnt_show_window"), include_est=include_est)
        times = [float(datetime.timestamp(x.measure_dt)) for x in qnt_states]
        values = [x.quantity for x in qnt_states]
        self.graphWidget.plot(times, values, symbol="o")

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

        self.graphWidget.plot([qnt_state_dt, qnt_state_dt+remaining_time], [qnt_state[0].quantity, 0], pen=pen)
