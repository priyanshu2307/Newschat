from typing import List, Dict, Any
from rag.embeddings import EmbeddingModel
from rag.vector_store import VectorStore
from rag.llm import LLMService
from services.session_service import SessionService
from config import TOP_K

class ChatService:
    """Service for handling chat interactions."""
    
    def __init__(self, 
                 embedding_model: EmbeddingModel,
                 vector_store: VectorStore,
                 llm_service: LLMService,
                 session_service: SessionService):
        """Initialize the chat service.
        
        Args:
            embedding_model: Embedding model
            vector_store: Vector store
            llm_service: LLM service
            session_service: Session service
        """
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.llm_service = llm_service
        self.session_service = session_service
    
    def process_message(self, session_id: str, message: str) -> str:
        """Process a user message and generate a response.
        
        Args:
            session_id: Session ID
            message: User message
            
        Returns:
            Assistant response
        """
        # Add user message to history
        self.session_service.add_message(session_id, {
            "role": "user",
            "content": message
        })

        
        # Get chat history
        history = self.session_service.get_chat_history(session_id)
        
        # Generate query embedding
        query_embedding = self.embedding_model._get_embeddings(message)[0]
        
        # Retrieve relevant contexts
        search_results = self.vector_store.search(query_embedding, top_k=TOP_K)
        contexts = search_results["documents"][0]
        
        # Generate response
        response = self.llm_service.generate_response(
            query=message,
            contexts=contexts,
            chat_history=history[:-1]  # Exclude the latest user message
        )
        
        # Add assistant response to history
        self.session_service.add_message(session_id, {
            "role": "user",
            "content": message
        })

        
        return response
    
    def get_chat_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get chat history for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            List of chat messages
        """
        return self.session_service.get_chat_history(session_id)
    
    def clear_chat_history(self, session_id: str):
        """Clear chat history for a session.
        
        Args:
            session_id: Session ID
        """
        self.session_service.clear_session(session_id)