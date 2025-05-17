import json
import feedparser
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import os
import uuid
from .embeddings import EmbeddingModel
from .vector_store import VectorStore

class ArticleIngestion:
    """Service for ingesting news articles."""
    
    def __init__(self, 
                 embedding_model: EmbeddingModel,
                 vector_store: VectorStore,
                 data_path: str = "./data/articles.json"):
        """Initialize the article ingestion service.
        
        Args:
            embedding_model: Embedding model
            vector_store: Vector store
            data_path: Path to save/load articles
        """
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.data_path = data_path
    
    def ingest_from_file(self) -> int:
        """Ingest articles from a local JSON file.
        
        Returns:
            Number of articles ingested
        """
        # Check if file exists
        if not os.path.exists(self.data_path):
            return 0
            
        # Load articles from file
        with open(self.data_path, 'r') as f:
            articles = json.load(f)
            
        # Process and add articles
        return self.process_articles(articles)
    
    def ingest_from_rss(self, rss_url: str) -> int:
        """Ingest articles from an RSS feed.
        
        Args:
            rss_url: URL of the RSS feed
            
        Returns:
            Number of articles ingested
        """
        # Parse the RSS feed
        feed = feedparser.parse(rss_url)
        
        # Extract articles
        articles = []
        for entry in feed.entries[:50]:  # Limit to 50 articles
            article = {
                "title": entry.title,
                "content": entry.get("summary", ""),
                "url": entry.link,
                "published": entry.get("published", ""),
                "source": feed.feed.title
            }
            
            # Try to get full content if only summary is available
            if len(article["content"]) < 500 and article["url"]:
                try:
                    full_content = self._fetch_article_content(article["url"])
                    if full_content:
                        article["content"] = full_content
                except Exception as e:
                    print(f"Error fetching content for {article['url']}: {e}")
            
            articles.append(article)
        
        # Save articles to file
        self._save_articles(articles)
        
        # Process and add articles
        return self.process_articles(articles)
    
    def _fetch_article_content(self, url: str) -> Optional[str]:
        """Fetch article content from URL.
        
        Args:
            url: Article URL
            
        Returns:
            Article content or None if failed
        """
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract main content (this is a simple implementation)
                # For real use, you'd need more sophisticated extraction
                paragraphs = soup.find_all('p')
                content = ' '.join([p.get_text() for p in paragraphs])
                
                return content
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            
        return None
    
    def _save_articles(self, articles: List[Dict[str, Any]]):
        """Save articles to file.
        
        Args:
            articles: List of article dictionaries
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        
        # Save articles
        with open(self.data_path, 'w') as f:
            json.dump(articles, f)
    
    def process_articles(self, articles: List[Dict[str, Any]]) -> int:
        """Process articles and add to vector store.
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            Number of articles processed
        """
        # Prepare documents, metadata, and IDs
        documents = []
        metadatas = []
        ids = []
        
        for article in articles:
            # Create document by combining title and content
            document = f"{article['title']}\n\n{article['content']}"
            documents.append(document)
            
            # Create metadata (exclude content to save space)
            metadata = {
                "title": article["title"],
                "url": article.get("url", ""),
                "published": article.get("published", ""),
                "source": article.get("source", "")
            }
            metadatas.append(metadata)
            
            # Generate ID
            doc_id = f"doc_{uuid.uuid4()}"
            ids.append(doc_id)
        
        # Generate embeddings
        embeddings = self.embedding_model._get_embeddings(documents)
        
        # Add to vector store
        self.vector_store.add_documents(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        return len(documents)