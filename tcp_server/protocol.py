from dataclasses import dataclass
from typing import Optional

@dataclass
class Response:
    status: str
    message: str
    data: Optional[dict] = None

class Protocol:
    @staticmethod
    def handle_command(command: str, params: str = "") -> Response:
        command = command.upper()
        
        if command == "PING":
            return Response("OK", "PONG")
            
        elif command == "ECHO":
            return Response("OK", params)
            
        elif command == "TIME":
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M:%S")
            return Response("OK", f"Current time is {current_time}")
            
        elif command == "INFO":
            server_info = {
                "name": "Python TCP Server",
                "version": "1.0.0",
                "protocol": "Custom TCP"
            }
            return Response("OK", "Server information", server_info)
            
        return Response("ERROR", "Unknown command")