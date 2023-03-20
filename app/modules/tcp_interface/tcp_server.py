import socketserver, socket
from utils.events.event_bus import EventBus
import json
from threading import Thread


def handle(data):
    data = json.loads(data.strip().decode("utf-8"))

    event_type = data["event_type"]
    del data["event_type"]
    print(event_type)
    match event_type:
        case "load":
            EventBus.invoke("alumina_load", **data)
        case "feed":
            EventBus.invoke("alumina_feed", **data)
        case "input":
            EventBus.invoke("input", **data)


def listener(client, address):
    print("Accepted connection from: ", address)
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            else:
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


def serve():
    EventBus.add_event("alumina_load")
    EventBus.add_event("alumina_feed")
    EventBus.add_event("input")
    while True:
        print("Server is listening for connections...")
        client, address = s.accept()
        client.send(b"0")
        th.append(Thread(target=listener, args=(client, address)).start())
    s.close()
