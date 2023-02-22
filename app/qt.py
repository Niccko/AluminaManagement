from db import init_db
init_db()

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import * 
from modules.bunker_management.bunker_manager import BunkerManager
import sys
from utils.events.event_bus import EventBus
from modules.tcp_interface.tcp_server import TCPServer
from modules.bunker_management.bunker_manager import BunkerManager
from modules.configuration import config

from random import randint


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(100, 100, 600, 400)
        self.bunker_manager = BunkerManager()
        

        self.UiComponents()
        self.show()

    def UiComponents(self):
        bunkers = self.bunker_manager.get_bunker_states()
        for i, bunker in enumerate(bunkers):
            bar = QProgressBar(self)
            bar.setGeometry(90*i+50, 50, 40, 200)
            if bunker and bunker[2]:
                bar.setValue(int(100*bunker[2]/bunker[1]))
                print(bunker)
                print(int(100*bunker[2]/bunker[1]))
            bar.setOrientation(QtCore.Qt.Vertical)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
