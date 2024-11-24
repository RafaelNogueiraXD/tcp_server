import socket
import json
from typing import Tuple
from .protocol import Protocol

class ConnectionHandler:
    def __init__(self, client_socket: socket.socket, address: Tuple[str, int]):
        self.client_socket = client_socket
        self.address = address
        self.protocol = Protocol()
        
    def handle_client(self):
        """Gerencia a conexão com um cliente específico."""
        try:
            while True:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                    
                # Parse do comando
                parts = data.strip().split(maxsplit=1)
                command = parts[0]
                params = parts[1] if len(parts) > 1 else ""
                
                # Processa o comando
                response = self.protocol.handle_command(command, params)
                
                # Envia a resposta
                response_data = json.dumps(response.__dict__)
                self.client_socket.send(f"{response_data}\n".encode('utf-8'))
                
        except Exception as e:
            print(f"Error handling client {self.address}: {e}")
        finally:
            self.client_socket.close()
            print(f"Connection closed with {self.address}")
