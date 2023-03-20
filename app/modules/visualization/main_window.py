from PyQt5.QtWidgets import *
from modules.visualization import design
from utils.events.event_bus import EventBus
from modules.bunker_management.bunker_manager import BunkerManager
from PyQt5 import QtWidgets
from utils.events.event_bus import EventBus
from modules.visualization.bunker_widget import BunkerWidget
from modules.visualization.graph_widget import QuantityGraph
import datetime
from modules.visualization.config_window import ConfigWindow


class MainWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.selected_bunker = None

        self.bunker_manager = BunkerManager()
        self.bunker_widget = BunkerWidget(self.bar_label)
        self.quantity_graph = QuantityGraph(self.qnt_graph)

        self.btn_editConfig.clicked.connect(self.open_config_window)

        self.bunker_widget.paintEvent(self.bunker_manager.get_aas_states())

        self.close_bunker.clicked.connect(lambda: self.update_selected(None))

        self.redraw()
        EventBus.subscribe("bunkers_updated", self.redraw)
        EventBus.subscribe("selectedBunkerChanged",lambda bunker_id: self.update_selected(bunker_id))

        self.show()

    def redraw(self):
        self.qnt_graph.setEnabled(self.selected_bunker is not None)
        self.close_bunker.setEnabled(self.selected_bunker is not None)
        self.qnt_graph.setVisible(self.selected_bunker is not None)
        self.close_bunker.setVisible(self.selected_bunker is not None)
        self.quantity_graph.graphWidget.clear()
        self.bunker_widget.paintEvent(self.bunker_manager.get_aas_states())
        qnt_states = self.bunker_manager.get_quantity_info(
            self.selected_bunker)
        times = list(
            map(lambda x: float(datetime.datetime.timestamp(x.measure_dt)), qnt_states))
        values = list(map(lambda x: x.value, qnt_states))
        self.quantity_graph.graphWidget.plot(times, values, symbol="o")

        self.update()

    def open_config_window(self):
        self.config_window = ConfigWindow()
        self.config_window.show()

    def update_selected(self, bunker_id):
        self.selected_bunker = bunker_id
        self.redraw()
