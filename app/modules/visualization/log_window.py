from modules.visualization import design
from PyQt5 import QtWidgets, Qt, QtCore
from modules.visualization import des_logs
from modules.logger.logger import get_logs
from datetime import datetime


class LogWindow(QtWidgets.QMainWindow, des_logs.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(LogWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setWindowTitle("Logs")

        self.btn_refresh.clicked.connect(self.update_logs)
        self.chk_now.clicked.connect(self.now_clicked)
        self.tbl_logs.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tbl_logs.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tbl_logs.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

    def update_logs(self):
        logs = get_logs(
            self.dttmStart.dateTime().toPyDateTime(),
            self.dttmEnd.dateTime().toPyDateTime() if not self.chk_now.isChecked() else datetime.now(),
            include=[
                "INFO" if self.chk_info.isChecked() else "",
                "WARNING" if self.chk_warn.isChecked() else "",
                "ERROR" if self.chk_error.isChecked() else "",
            ]
        )
        for i in range(self.tbl_logs.rowCount() - 1, -1, -1):
            self.tbl_logs.removeRow(i)
        for i, log in enumerate(logs):
            self.tbl_logs.insertRow(i)
            self.tbl_logs.setItem(i, 0, Qt.QTableWidgetItem(str(log.log_dt)))
            self.tbl_logs.setItem(i, 1, Qt.QTableWidgetItem(str(log.log_type)))
            self.tbl_logs.setItem(i, 2, Qt.QTableWidgetItem(str(log.description)))

    def now_clicked(self):
        self.dttmEnd.setDateTime(datetime.now())
        self.dttmEnd.setEnabled(not self.chk_now.isChecked())
