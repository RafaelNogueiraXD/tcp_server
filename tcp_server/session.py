from dataclasses import dataclass
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

@dataclass
class Session:
    id: str
    client_address: tuple[str, int]
    created_at: datetime
    last_activity: datetime
    data: Dict[str, Any]
    
    @classmethod
    def create(cls, client_address: tuple[str, int]) -> 'Session':
        """Cria uma nova sessão para um cliente."""
        return cls(
            id=str(uuid.uuid4()),
            client_address=client_address,
            created_at=datetime.now(),
            last_activity=datetime.now(),
            data={}
        )
    
    def update_activity(self):
        """Atualiza o timestamp da última atividade."""
        self.last_activity = datetime.now()
    
    def set_data(self, key: str, value: Any):
        """Armazena dados na sessão."""
        self.data[key] = value
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """Recupera dados da sessão."""
        return self.data.get(key, default)

class SessionManager:
    def __init__(self):
        self._sessions: Dict[str, Session] = {}
    
    def create_session(self, client_address: tuple[str, int]) -> Session:
        """Cria e registra uma nova sessão."""
        session = Session.create(client_address)
        self._sessions[session.id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Recupera uma sessão pelo ID."""
        return self._sessions.get(session_id)
    
    def get_session_by_address(self, client_address: tuple[str, int]) -> Optional[Session]:
        """Recupera uma sessão pelo endereço do cliente."""
        for session in self._sessions.values():
            if session.client_address == client_address:
                return session
        return None
    
    def remove_session(self, session_id: str):
        """Remove uma sessão."""
        self._sessions.pop(session_id, None)
    
    def cleanup_inactive(self, max_inactive_minutes: int = 30):
        """Remove sessões inativas."""
        now = datetime.now()
        inactive_sessions = [
            session_id for session_id, session in self._sessions.items()
            if (now - session.last_activity).total_minutes() > max_inactive_minutes
        ]
        for session_id in inactive_sessions:
            self.remove_session(session_id)