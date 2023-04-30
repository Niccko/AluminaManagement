import socket
import threading


def write(client, message):
    client.sendall((message + '#').encode('utf-8'))


def start_client(receive_handler, args=()):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    receive_thread = threading.Thread(target=receive_handler, args=args)
    return client, receive_thread
