import google.generativeai as genai
from typing import List, Dict, Any
from config import GEMINI_API_KEY

class LLMService:
    """Service for interacting with Gemini LLM API."""
    
    def __init__(self):
        """Initialize the LLM service."""
        # Configure the Gemini API
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def generate_response(self, query: str, contexts: List[str], 
                          chat_history: List[Dict[str, str]] = None) -> str:
        """Generate a response based on query and contexts.
        
        Args:
            query: User query
            contexts: List of context passages
            chat_history: List of chat history messages
            
        Returns:
            LLM response
        """
        # Default empty chat history
        if chat_history is None:
            chat_history = []
            
        # Format the context
        context_text = "\n\n".join([f"Article: {ctx}" for ctx in contexts])
        
        # Build the prompt
        system_prompt = f"""You are a helpful assistant that answers questions about news articles.
Base your answers solely on the provided context information.
If you don't know the answer based on the provided context, say "I don't have enough information to answer that question."
Be concise but comprehensive in your responses.

Context information:
{context_text}
"""

        # Create the chat session with history
        chat = self.model.start_chat(history=[])
        
        # Add system prompt
        chat.send_message(system_prompt)
        
        # Add chat history
        for message in chat_history:
            role = message["role"]
            content = message["content"]
            if role == "user":
                chat.send_message(content)
            elif role == "assistant":
                # This is a bit of a hack since Gemini API doesn't support
                # directly setting assistant messages in history
                user_msg = "Please remember your last response was: " + content
                chat.send_message(user_msg)
        
        # Send the user query and get response
        response = chat.send_message(query)
        
        return response.text