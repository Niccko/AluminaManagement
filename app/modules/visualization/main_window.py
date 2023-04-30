from modules import bunker_manager
from modules.visualization import design
from PyQt5 import QtWidgets, Qt, QtCore
import time

from utils.events.event_bus import EventBus
from modules.visualization.bunker_widget import BunkerWidget
from modules.visualization.graph_widget import QuantityGraph
from datetime import datetime, timedelta
from modules.visualization.config_window import ConfigWindow
from modules.visualization.process_window import ProcessWindow
from modules.estimate import est_devastation
from modules.process_management import get_current_process
import global_vars


class MainWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.process_window = ProcessWindow()
        self.process_window.move(self.width()+400, 400)
        print(self.pos().x())
        print(self.pos().y())
        self.process_window.show()

        self.selected_bunker = None
        self.last_updated = 0

        self.bunker_widget = BunkerWidget(self.bar_label, 1)
        self.quantity_graph = QuantityGraph(self.main_panel)
        self.big_bunker_widget = BunkerWidget(self.lbl_main_bunkers, 2)

        self.btn_editConfig.triggered.connect(self.open_config_window)
        self.close_bunker.clicked.connect(lambda: self.update_selected(None))
        self.update_selected(None)

        self.tbl_feeds.horizontalHeader().resizeSection(0, 280)
        self.tbl_feeds.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tbl_feeds.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.tbl_loads.horizontalHeader().resizeSection(0, 250)
        self.tbl_loads.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.tbl_loads.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.tbl_loads.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.redraw()
        EventBus.subscribe("bunkers_updated", self.redraw)
        EventBus.subscribe("selectedBunkerChanged", lambda bunker_id: self.update_selected(bunker_id))

        self.show()

    def moveEvent(self, event) -> None:
        super(MainWindow, self).moveEvent(event)

    def redraw(self, force=False):
        time_remaining = 0
        if not force and time.time() - self.last_updated < 0.3:
            return
        self.process_window.redraw()
        process = get_current_process()
        if process:
            self.lbl_processId_value.setText(str(process.process_id))
            self.lbl_processDTTM_value.setText(str(process.start_dttm))

        self.bunker_widget.container.pixmap().fill(QtCore.Qt.white)
        self.big_bunker_widget.container.pixmap().fill(QtCore.Qt.white)
        self.draw_bunkers()
        self.update_event_tables()

        if self.selected_bunker:
            bunker = bunker_manager.get_bunker(self.selected_bunker)
            bunker_state = bunker_manager.get_last_bunker_state(self.selected_bunker)
            last_feed = bunker_manager.get_last_alumina_move("FEED", bunker_id=bunker.bunker_id)
            rem = est_devastation(bunker_id=self.selected_bunker)
            if rem:
                time_remaining = round(rem, 2)
                end_time = (bunker_state.measure_dt + timedelta(seconds=time_remaining)).strftime("%Y-%m-%d %H:%M:%S")
                self.lbl_timeRemainig_value.setText(f"{str(time_remaining)} сек ({end_time})")
                self.lbl_bunkerId_value.setText(str(self.selected_bunker))

            last_load = bunker_manager.get_last_alumina_move("LOAD", bunker_id=self.selected_bunker)
            last_feed = bunker_manager.get_last_alumina_move("FEED", bunker_id=self.selected_bunker)
            if last_feed:
                feed_dttm = str(last_feed.feed_dt.strftime("%Y-%m-%d %H:%M:%S"))
                quantity = str(int(last_feed.quantity))
                self.lbl_lastFeed_value.setText(f'{feed_dttm} ({quantity} кг)')
            if last_load:
                load_dttm = str(last_load.load_dt.strftime("%Y-%m-%d %H:%M:%S"))
                quantity = str(int(last_load.quantity))
                source = last_load.source_bunker_id
                self.lbl_lastLoad_value.setText(f'{load_dttm} ({quantity} кг) - source: {source}')
            self.quantity_graph.graphWidget.clear()
            self.quantity_graph.draw_prediction(self.selected_bunker, time_remaining)
            self.quantity_graph.draw(self.selected_bunker)

            self.lbl_capacity_value.setText(f'{str(int(bunker.capacity))} кг')
            self.lbl_quantity_value.setText(f'{str(int(bunker_state.quantity))} кг')
            consumption = bunker_manager.get_mean_consumption(self.selected_bunker)
            self.lbl_dayCons_value.setText(str(consumption.get("day")))
            self.lbl_monthCons_value.setText(str(consumption.get("month")))

        self.update()
        self.last_updated = time.time()

    def draw_bunkers(self):
        self.bunker_widget.paintEvent(bunker_manager.get_bunkers_states(is_aas=True))

        estimate_bunkers_color = Qt.QColor(0, 176, 246)
        estimate_bunkers_color.setAlpha(80)
        self.big_bunker_widget.paintEvent(
            bunker_manager.get_bunkers_states(is_aas=False, include_est=2),
            estimate_bunkers_color
        )
        self.big_bunker_widget.paintEvent(
            bunker_manager.get_bunkers_states(is_aas=False, include_est=0),
            Qt.QColor(0, 191, 124)
        )

    def open_config_window(self):
        self.config_window = ConfigWindow()
        self.config_window.show()

    def open_process_window(self):
        self.process_window = ProcessWindow()
        self.process_window.show()

    def update_selected(self, bunker_id):
        self.selected_bunker = bunker_id
        self.main_panel.setEnabled(self.selected_bunker is not None)
        self.lbl_main_bunkers.setEnabled(self.selected_bunker is None)
        self.close_bunker.setEnabled(self.selected_bunker is not None)
        self.main_panel.setVisible(self.selected_bunker is not None)
        self.lbl_main_bunkers.setVisible(self.selected_bunker is None)
        self.close_bunker.setVisible(self.selected_bunker is not None)
        # self.frm_common_info.setVisible(self.selected_bunker is None)

        for child_widget in self.gridLayoutWidget.findChildren(QtWidgets.QWidget):
            child_widget.setVisible(self.selected_bunker is not None)
        self.redraw(force=True)

    def update_event_tables(self):
        for i in range(self.tbl_loads.rowCount() - 1, -1, -1):
            self.tbl_loads.removeRow(i)
        for i in range(self.tbl_feeds.rowCount() - 1, -1, -1):
            self.tbl_feeds.removeRow(i)
        loads = bunker_manager.get_last_alumina_move("LOAD", row_limit=16)
        feeds = bunker_manager.get_last_alumina_move("FEED", row_limit=16)
        for i, load in enumerate(loads):
            self.tbl_loads.insertRow(i)
            self.tbl_loads.setItem(i, 0, Qt.QTableWidgetItem(str(load.load_dt)))
            self.tbl_loads.setItem(i, 1, Qt.QTableWidgetItem(str(load.bunker_id)))
            self.tbl_loads.setItem(i, 2, Qt.QTableWidgetItem(str(load.quantity)))
            self.tbl_loads.setItem(i, 3, Qt.QTableWidgetItem(str(load.source_bunker_id)))
        for i, feed in enumerate(feeds):
            self.tbl_feeds.insertRow(i)
            self.tbl_feeds.setItem(i, 0, Qt.QTableWidgetItem(str(feed.feed_dt)))
            self.tbl_feeds.setItem(i, 1, Qt.QTableWidgetItem(str(feed.bunker_id)))
            self.tbl_feeds.setItem(i, 2, Qt.QTableWidgetItem(str(feed.quantity)))

        self.update()
