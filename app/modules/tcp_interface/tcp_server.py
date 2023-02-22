import socketserver
from utils.events.event_bus import EventBus
import os, json

class TCPHandler(socketserver.BaseRequestHandler):
    EventBus.add_event("alumina_load")
    EventBus.add_event("alumina_feed")

    def handle(self): 
        self.data = self.request.recv(1024).strip().decode("utf-8")
        self.data = json.loads(self.data)
        event_type = self.data["event_type"]
        del self.data["event_type"]
        match event_type:
            case "load":
                EventBus.invoke("alumina_load", **self.data)
            case "feed":
                EventBus.invoke("alumina_feed", **self.data)
        
        self.request.sendall(bytes("1".encode("utf-8")))
        

class TCPServer:
    EventBus.add_event("tcp_ready")
    socketserver.TCPServer.allow_reuse_address = True
    def start(self):
        self.server = None
        HOST, PORT = "localhost", 9999
        
        self.server = socketserver.TCPServer((HOST, PORT), TCPHandler)
        EventBus.invoke("tcp_ready")
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
           
                
