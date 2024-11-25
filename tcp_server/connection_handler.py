import socket
import json
from typing import Tuple
from .protocol import Protocol
from .session import SessionManager

class ConnectionHandler:
    def __init__(self, client_socket: socket.socket, address: tuple[str, int], session_manager: SessionManager):
        self.client_socket = client_socket
        self.address = address
        self.protocol = Protocol()
        self.session_manager = session_manager
        self.session = self.session_manager.create_session(address)
        
    def handle_client(self):
        """Gerencia a conexão com um cliente específico."""
        try:
            print(f"New session created: {self.session.id} for client {self.address}")
            
            while True:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                # Atualiza a atividade da sessão
                self.session.update_activity()
                
                # Parse do comando
                parts = data.strip().split(maxsplit=1)
                command = parts[0]
                params = parts[1] if len(parts) > 1 else ""
                
                # Processa o comando
                response = self.protocol.handle_command(command, params, self.session)
                
                # Envia a resposta
                response_data = json.dumps(response.__dict__)
                self.client_socket.send(f"{response_data}\n".encode('utf-8'))
                
        except Exception as e:
            print(f"Error handling client {self.address}: {e}")
        finally:
            self.session_manager.remove_session(self.session.id)
            self.client_socket.close()
            print(f"Session {self.session.id} closed for client {self.address}")