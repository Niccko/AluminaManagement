from PyQt5.QtWidgets import *
from random import randint, choice
from modules.visualization import design
from modules.configuration import config
from modules.tcp_interface.tcp_server import TCPServer
from utils.events.event_bus import EventBus
import sys
from modules.bunker_management.bunker_manager import BunkerManager
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore, uic, QtGui
from math import sin
from utils.events.event_bus import EventBus
from modules.visualization.bunker_widget import BunkerWidget
from modules.visualization.graph_widget import QuantityGraph
import datetime
from pprint import pprint


class MainWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.selected_bunker = None

        self.bunker_manager = BunkerManager()
        self.bunker_widget = BunkerWidget(self.bar_label)
        self.quantity_graph = QuantityGraph(self.qnt_graph)

        self.bunker_widget.paintEvent(self.bunker_manager.get_bunker_states())

        self.close_bunker.clicked.connect(lambda: self.update_selected(None))
        

        self.redraw()
        EventBus.subscribe("bunkers_updated", self.redraw)
        EventBus.subscribe("selectedBunkerChanged", lambda bunker_id: self.update_selected(bunker_id))

        self.show()

    def redraw(self):
        self.qnt_graph.setEnabled(self.selected_bunker is not None)
        self.close_bunker.setEnabled(self.selected_bunker is not None)
        self.qnt_graph.setVisible(self.selected_bunker is not None)
        self.close_bunker.setVisible(self.selected_bunker is not None)
        self.quantity_graph.graphWidget.clear()
        self.bunker_widget.paintEvent(self.bunker_manager.get_bunker_states())
        qnt_states = self.bunker_manager.get_quantity_info(self.selected_bunker)
        times = list(map(lambda x: float(datetime.datetime.timestamp(x.measure_dt)), qnt_states))
        values = list(map(lambda x: x.quantity, qnt_states))
        self.quantity_graph.graphWidget.plot(times, values, symbol = "o")
        
        self.update()

    def update_selected(self, bunker_id):
        self.selected_bunker = bunker_id
        self.redraw()

    