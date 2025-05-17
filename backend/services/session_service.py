import json
import uuid
import time
from typing import Dict, Any, List

class SessionService:
    def __init__(self):
        """Initialize the session service with an in-memory store instead of Redis."""
        self.sessions = {}  # In-memory store
        self.session_expiry = 3600  # Session expiry in seconds (1 hour)
    
    def create_session(self) -> str:
        """Create a new chat session.
        
        Returns:
            str: A unique session identifier
        """
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "created_at": time.time(),
            "updated_at": time.time(),
            "messages": []
        }
        return session_id
    
    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get session data by ID.
        
        Args:
            session_id: The unique session identifier
            
        Returns:
            Dict containing session data
            
        Raises:
            ValueError: If session does not exist or has expired
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
            
        session = self.sessions[session_id]
        
        # Check if session has expired
        if time.time() - session["updated_at"] > self.session_expiry:
            del self.sessions[session_id]
            raise ValueError(f"Session {session_id} has expired")
            
        return session
    
    def update_session(self, session_id: str, data: Dict[str, Any]) -> None:
        """Update session data.
        
        Args:
            session_id: The unique session identifier
            data: The data to update
            
        Raises:
            ValueError: If session does not exist
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
            
        self.sessions[session_id].update(data)
        self.sessions[session_id]["updated_at"] = time.time()
    
    def add_message(self, session_id: str, message: Dict[str, Any]) -> None:
        """Add a message to the session history.
        
        Args:
            session_id: The unique session identifier
            message: The message data including role and content
            
        Raises:
            ValueError: If session does not exist
        """
        session = self.get_session(session_id)
        
        if "messages" not in session:
            session["messages"] = []
            
        session["messages"].append(message)
        self.update_session(session_id, {"messages": session["messages"]})
    
    def get_message_history(self, session_id: str) -> list:
        """Get all messages for a session.
        
        Args:
            session_id: The unique session identifier
            
        Returns:
            List of message objects
            
        Raises:
            ValueError: If session does not exist
        """
        session = self.get_session(session_id)
        return session.get("messages", [])
    
    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists and hasn't expired.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if session exists and is valid, False otherwise
        """
        if session_id not in self.sessions:
            return False

        session = self.sessions[session_id]
        if time.time() - session["updated_at"] > self.session_expiry:
            del self.sessions[session_id]
            return False

        return True
    
    def get_chat_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all messages for a session.
        
        Args:
            session_id: The unique session identifier
            
        Returns:
            List of message objects
            
        Raises:
            ValueError: If session does not exist
        """
        session = self.get_session(session_id)
        return session.get("messages", [])
    
    def clear_session(self, session_id: str) -> None:
        """Remove a session entirely."""
        if session_id in self.sessions:
            del self.sessions[session_id]
