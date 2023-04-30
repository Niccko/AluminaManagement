from PyQt5 import QtWidgets, Qt
from modules.visualization import process
import global_vars
from modules.estimate import check_devastation


class ProcessWindow(QtWidgets.QMainWindow, process.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(ProcessWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.queue_timer = Qt.QTimer()
        self.queue_timer.timeout.connect(self.redraw_queue)
        self.queue_timer.setInterval(5000)
        self.queue_timer.start()

    def redraw(self):
        self.lbl_dbConnected_value.setText(str(global_vars.db_connected))
        self.lbl_hardwareConnected_value.setText(str(global_vars.hardware_connected))

        self.update()

    def redraw_queue(self):
        load_queue = check_devastation()
        for i in range(self.tbl_loadQueue.rowCount() - 1, -1, -1):
            self.tbl_loadQueue.removeRow(i)
        for i, element in enumerate(load_queue):
            self.tbl_loadQueue.insertRow(i)
            self.tbl_loadQueue.setItem(i, 0, Qt.QTableWidgetItem(str(element["bunker_id"])))
