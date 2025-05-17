from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import os

from config import API_HOST, API_PORT, DATA_PATH
from rag.embeddings import EmbeddingModel
from rag.vector_store import VectorStore
from rag.llm import LLMService
from rag.article_ingestion import ArticleIngestion
from services.session_service import SessionService
from services.chat_service import ChatService

# Create FastAPI app
app = FastAPI(title="NewsChat API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
embedding_model = EmbeddingModel()
vector_store = VectorStore()
llm_service = LLMService()
session_service = SessionService()

# Initialize services
article_ingestion = ArticleIngestion(
    embedding_model=embedding_model,
    vector_store=vector_store,
    data_path=DATA_PATH
)
chat_service = ChatService(
    embedding_model=embedding_model,
    vector_store=vector_store,
    llm_service=llm_service,
    session_service=session_service
)

# Request/response models
class SessionResponse(BaseModel):
    session_id: str

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str

class ChatHistoryResponse(BaseModel):
    history: List[Dict[str, str]]

class StatusResponse(BaseModel):
    status: str
    message: str
    articles_count: int

# Dependency to check if session exists
async def validate_session(session_id: str):
    if not session_service.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    return session_id

# Routes
@app.post("/sessions", response_model=SessionResponse)
async def create_session():
    """Create a new chat session."""
    session_id = session_service.create_session()
    return {"session_id": session_id}

@app.get("/sessions/{session_id}", response_model=ChatHistoryResponse, dependencies=[Depends(validate_session)])
async def get_session_history(session_id: str):
    """Get chat history for a session."""
    history = chat_service.get_chat_history(session_id)
    return {"history": history}

@app.delete("/sessions/{session_id}", response_model=StatusResponse, dependencies=[Depends(validate_session)])
async def clear_session(session_id: str):
    """Clear a chat session."""
    chat_service.clear_chat_history(session_id)
    return {
        "status": "success",
        "message": "Session cleared",
        "articles_count": vector_store.get_collection_count()
    }

@app.post("/sessions/{session_id}/messages", response_model=MessageResponse, dependencies=[Depends(validate_session)])
async def send_message(session_id: str, request: MessageRequest):
    """Send a message to the chatbot."""
    response = chat_service.process_message(session_id, request.message)
    return {"response": response}

@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get system status."""
    return {
        "status": "online",
        "message": "System is operational",
        "articles_count": vector_store.get_collection_count()
    }

@app.post("/ingest/file", response_model=StatusResponse)
async def ingest_from_file(background_tasks: BackgroundTasks):
    """Ingest articles from file."""
    # Run ingestion in background
    background_tasks.add_task(article_ingestion.ingest_from_file)
    
    return {
        "status": "processing",
        "message": "Started ingesting articles from file",
        "articles_count": vector_store.get_collection_count()
    }

@app.post("/ingest/rss", response_model=StatusResponse)
async def ingest_from_rss(rss_url: str, background_tasks: BackgroundTasks):
    """Ingest articles from RSS feed."""
    # Run ingestion in background
    background_tasks.add_task(article_ingestion.ingest_from_rss, rss_url)
    
    return {
        "status": "processing",
        "message": f"Started ingesting articles from RSS: {rss_url}",
        "articles_count": vector_store.get_collection_count()
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    # Load articles from file on startup
    article_count = article_ingestion.ingest_from_file()
    print(f"Loaded {article_count} articles from file")

# Main entry point
if __name__ == "__main__":
    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=True)