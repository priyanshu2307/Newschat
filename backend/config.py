from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_TTL = int(os.getenv("REDIS_TTL", "86400"))  # 24 hours default TTL

# Vector DB Configuration
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./chroma_db")

# LLM Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# RAG Configuration
TOP_K = int(os.getenv("TOP_K", "3"))  # Number of passages to retrieve
DATA_PATH = os.getenv("DATA_PATH", "./data/articles.json")

# Session Configuration
SESSION_EXPIRY = int(os.getenv("SESSION_EXPIRY", "3600"))  # 1 hour

# Jina Configuration
JINA_API_KEY = os.getenv("JINA_API_KEY", "")