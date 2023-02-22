import socket
import json
import time


HOST, PORT = "localhost", 9999
data = json.dumps(
    {
        "event_type": "feed",
        "bunker_id": 1,
        "quantity": 10
    }
)


while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))
    received = str(sock.recv(1024), "utf-8")
    print(received)
    sock.close()
    time.sleep(1)
