from dataclasses import dataclass
from typing import Optional
from .session import *

@dataclass
class Response:
    status: str
    message: str
    data: Optional[dict] = None

class Protocol:
    @staticmethod
    def handle_command(command: str, params: str = "", session: Optional[Session] = None) -> Response:
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
            if session:
                server_info = {
                    "name": "Python TCP Server",
                    "version": "1.0.0",
                    "protocol": "Custom TCP",
                    "session_id": session.id,
                    "session_created": session.created_at.isoformat(),
                    "last_activity": session.last_activity.isoformat()
                }
            else:
                server_info = {
                    "name": "Python TCP Server",
                    "version": "1.0.0",
                    "protocol": "Custom TCP"
                }
            return Response("OK", "Server information", server_info)
            
        elif command == "SET" and session:
            try:
                key, value = params.split(maxsplit=1)
                session.set_data(key, value)
                return Response("OK", f"Value set for key: {key}")
            except ValueError:
                return Response("ERROR", "Invalid SET command format. Use: SET key value")
                
        elif command == "GET" and session:
            key = params.strip()
            value = session.get_data(key)
            if value is not None:
                return Response("OK", f"Value for {key}", {"value": value})
            return Response("ERROR", f"No value found for key: {key}")
            
        return Response("ERROR", "Unknown command")