import socket
import threading
from typing import List
from .config import Config
from .connection_handler import ConnectionHandler

class TCPServer:
    def __init__(self):
        self.config = Config()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients: List[threading.Thread] = []
        
    def start(self):
        """Inicia o servidor TCP."""
        try:
            # Configura e inicia o servidor
            self.server_socket.bind((self.config.HOST, self.config.PORT))
            self.server_socket.listen(self.config.MAX_CONNECTIONS)
            print(f"Server listening on {self.config.HOST}:{self.config.PORT}")
            
            while True:
                # Aceita novas conexões
                client_socket, address = self.server_socket.accept()
                print(f"New connection from {address}")
                
                # Cria um novo handler para a conexão
                handler = ConnectionHandler(client_socket, address)
                
                # Inicia uma nova thread para gerenciar a conexão
                client_thread = threading.Thread(
                    target=handler.handle_client,
                    daemon=True
                )
                client_thread.start()
                self.clients.append(client_thread)
                
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Limpa recursos e fecha conexões."""
        for client in self.clients:
            client.join(timeout=1.0)
        self.server_socket.close()
        print("Server shutdown complete")

if __name__ == "__main__":
    server = TCPServer()
    server.start()