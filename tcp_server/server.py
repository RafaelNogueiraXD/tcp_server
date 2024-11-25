import socket
import threading
from typing import List
from .config import Config
from .connection_handler import ConnectionHandler
from .session import SessionManager
import time

class TCPServer:
    def __init__(self):
        self.config = Config()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session_manager = SessionManager()
        self.clients: List[threading.Thread] = []
        
    def start(self):
        """Inicia o servidor TCP."""
        try:
            self.server_socket.bind((self.config.HOST, self.config.PORT))
            self.server_socket.listen(self.config.MAX_CONNECTIONS)
            print(f"Server listening on {self.config.HOST}:{self.config.PORT}")
            
            # Inicia thread para limpeza de sessões inativas
            cleanup_thread = threading.Thread(
                target=self._cleanup_sessions,
                daemon=True
            )
            cleanup_thread.start()
            
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"New connection from {address}")
                
                handler = ConnectionHandler(client_socket, address, self.session_manager)
                
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

    def _cleanup_sessions(self):
        """Thread para limpeza periódica de sessões inativas."""
        while True:
            self.session_manager.cleanup_inactive()
            time.sleep(300)

if __name__ == "__main__":
    server = TCPServer()
    server.start()