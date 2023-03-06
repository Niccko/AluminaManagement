from db import init_db
init_db()

from utils.events.event_bus import EventBus
from modules.tcp_interface.tcp_server import TCPServer
from modules.bunker_management.bunker_manager import BunkerManager
from modules.configuration import config
from modules.estimate.estimate import est_devastation
import threading, sys, time

from modules.visualization import MainWindow

from PyQt5 import QtWidgets



# def command_exec():
#     while True:
#         command = input(">")
#         match command:
#             case "shut":
#                 server.stop()
#                 break

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    threading.Thread(target=main).start()
    time.sleep(1)
    server = TCPServer()
    #threading.Thread(target=server.start).start()