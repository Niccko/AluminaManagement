import socket
import json
import time
from random import randint


HOST, PORT = "localhost", 9999

# for i in range(1, 71):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect((HOST, PORT))
#     data = json.dumps(
#         {
#             "event_type": "load",
#             "bunker_id": i,
#             "quantity": 200,
#             "type": 1
#         }
#     )
#     sock.sendall(bytes(data + "\n", "utf-8"))
#     received = str(sock.recv(1024), "utf-8")
#     sock.close()

while True:
    for i in range(1, 71):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        data = json.dumps(
            {
                "event_type": "feed",
                "bunker_id": i,
                "quantity": randint(0,3)
            }
        )
        sock.sendall(bytes(data + "\n", "utf-8"))
        received = str(sock.recv(1024), "utf-8")
        sock.close()
    time.sleep(0.01)
