import sys
import threading
import time

from PyQt5 import QtWidgets

from modules.tcp_server import serve
from modules.visualization import MainWindow


def main(done_event):
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec_()
    done_event.set()
    sys.exit()


done = threading.Event()

if __name__ == '__main__':
    threading.Thread(target=main, args=[done, ]).start()
    time.sleep(1)
    threading.Thread(target=serve, args=[done, ]).start()
