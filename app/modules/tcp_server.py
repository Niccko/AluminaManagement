import socket
from utils.events.event_bus import EventBus
import json
from threading import Thread
from modules.logger import *


def handle(data):
    str_data = data.strip().decode("utf-8")
    for chunk in str_data.split("#"):
        if not chunk:
            continue
        data = json.loads(chunk)
        event_type = data["event_type"]
        del data["event_type"]
        match event_type:
            case "load":
                EventBus.invoke("alumina_load", **data)
            case "feed":
                EventBus.invoke("alumina_feed", **data)
            case "input":
                EventBus.invoke("input", **data)
            case "process_start":
                EventBus.invoke("process_start")
            case "init_topology":
                EventBus.invoke("init_topology", data=data.get("data"))


def listener(client, address):
    info(f"Accepted connection from: {address}")
    try:
        while True:
            try:
                data = client.recv(32768)
                if not data:
                    continue
            except Exception as e:
                error("Связь с оборудованием потеряна")
                break
            handle(data)
            client.sendall(b"0")

    finally:
        client.close()


host = socket.gethostname()
port = 9999

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", port))
s.listen(1)
th = []


def serve(done):
    EventBus.add_event("alumina_load")
    EventBus.add_event("alumina_feed")
    EventBus.add_event("input")
    EventBus.add_event("process_start")
    EventBus.add_event("init_topology")
    while not done.is_set():
        info("Server is listening for connections...")
        client, address = s.accept()
        client.send(b"0")
        th.append(Thread(target=listener, args=(client, address)).start())
    s.close()
