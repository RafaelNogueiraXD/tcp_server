import socket
import threading
import pytest
import json
import time
from tcp_server.server import TCPServer

@pytest.fixture
def server():
    server = TCPServer()
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.1)  # Aguarda o servidor iniciar
    yield server
    server.cleanup()

def test_server_connection(server):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server.config.HOST, server.config.PORT))
    
    # Testa o comando PING
    client.send("PING\n".encode('utf-8'))
    response = json.loads(client.recv(1024).decode('utf-8'))
    assert response["status"] == "OK"
    assert response["message"] == "PONG"
    
    client.close()