import chromadb
from typing import List, Dict, Any
import os
from config import VECTOR_DB_PATH

class VectorStore:
    """Vector store for storing and retrieving embeddings."""
    
    def __init__(self, collection_name: str = "news_articles"):
        """Initialize the vector store.
        
        Args:
            collection_name: Name of the collection to use
        """
        # Make sure directory exists
        os.makedirs(VECTOR_DB_PATH, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(collection_name)
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}  # Use cosine similarity
            )
    
    def add_documents(self, documents: List[str], 
                      embeddings: List[List[float]], 
                      metadatas: List[Dict[str, Any]] = None,
                      ids: List[str] = None):
        """Add documents to the vector store.
        
        Args:
            documents: List of document texts
            embeddings: List of embedding vectors
            metadatas: List of metadata dictionaries
            ids: List of document IDs
        """
        if metadatas is None:
            metadatas = [{} for _ in documents]
            
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
            
        # Add documents to collection
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query_embedding: List[float], top_k: int = 3) -> Dict[str, Any]:
        """Search for similar documents.
        
        Args:
            query_embedding: Embedding vector for the query
            top_k: Number of results to return
            
        Returns:
            Dictionary of search results
        """
        # Query the collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        return results
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection.
        
        Returns:
            Number of documents
        """
        return self.collection.count()