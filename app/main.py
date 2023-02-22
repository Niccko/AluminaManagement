from db import init_db
init_db()

from utils.events.event_bus import EventBus
from modules.tcp_interface.tcp_server import TCPServer
from modules.bunker_management.bunker_manager import BunkerManager
from modules.configuration import config
from modules.estimate.estimate import est_devastation
import threading



def command_exec():
    while True:
        command = input(">")
        match command:
            case "shut":
                server.stop()
                break



manager = BunkerManager()

server = TCPServer()
threading.Thread(target=server.start).start()
threading.Thread(target=command_exec).start()
