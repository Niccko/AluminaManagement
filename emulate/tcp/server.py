from threading import Thread
from datetime import datetime
import socket
import os

from urllib.parse import urlparse

CONNECTIONS = []
conn_config_file = None
db = None


def start_server(port, num_connections):
    sock = socket.socket()
    sock.setblocking(1)
    sock.bind(('', port))
    sock.listen(num_connections)
    CONNECTIONS = []
    return sock



def process_message(conn, msg: str):
    if msg.startswith("[SEND SQL]"):
        msg = msg[11:]
        process_sql_query(msg)
    elif msg.startswith("[CONTROL]"):
        for connection in CONNECTIONS:
            print(msg.encode())
            connection.send(msg.encode("utf-8"))


def process_sql_query(msg):
    if msg.startswith("[SENSOR]"):
        msg = msg[9:].split(":")
        add_sensor_value(msg[0], msg[1])


def connection_thread(conn, chunk_size=1024):
    while True:
        try:
            data = conn.recv(chunk_size).decode()
            if data:
                process_message(conn, data)
        except Exception as e:
            print(f"Connection {conn} closed.")
            print(f"[EXCEPTION] {e}")
            conn.close()
            break


def wait_connection(sock):
    while True:
        conn, addr = sock.accept()
        print(f"Accepted connection from {addr}")
        CONNECTIONS.append(conn)
        Thread(target=connection_thread, args=(conn,)).start()


if __name__ == "__main__":
    sock = start_server(7777, 3)
    connect_db()
    wait_connection(sock)
