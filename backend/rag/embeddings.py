import os
import requests
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmbeddingModel:
    def __init__(self, model_name="jina-embeddings-v2-base-en"):
        """Initialize the Jina embedding model.
        
        Args:
            model_name: Name of the embedding model to use.
                       Default is "jina-embeddings-v2-base-en"
        """
        self.model_name = model_name
        # Get API key from environment variable
        self.api_key = os.getenv("JINA_API_KEY")
        if not self.api_key:
            raise ValueError("JINA_API_KEY not found in environment variables")
        
        # API endpoint
        self.api_url = "https://api.jina.ai/v1/embeddings"
        
    def embed_query(self, text):
        """Embed a single query text using Jina AI API.
        
        Args:
            text: The text to embed
            
        Returns:
            A numpy array containing the embedding
        """
        return self._get_embeddings([text])[0]
    
    def embed_documents(self, documents):
        """Embed a list of documents using Jina AI API.
        
        Args:
            documents: List of texts to embed
            
        Returns:
            A list of numpy arrays containing the embeddings
        """
        return self._get_embeddings(documents)
    
    def _get_embeddings(self, texts):
        """Get embeddings from Jina AI API.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embeddings as numpy arrays
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "input": texts,
            "model": self.model_name
        }
        
        response = requests.post(self.api_url, headers=headers, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"Error from Jina AI API: {response.text}")
        
        # Parse response
        result = response.json()
        embeddings = [np.array(data["embedding"]) for data in result["data"]]
        
        return embeddings
    
    def similarity(self, embedding1, embedding2):
        """Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))