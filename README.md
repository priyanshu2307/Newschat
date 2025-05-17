# 📰 News RAG Chatbot

A lean Retrieval-Augmented Generation starter kit that ingests RSS news, embeds with **Jina Embeddings**, stores vectors in **Qdrant**, and answers questions with context using **GPT-4o-mini**. Front‑end is **React + Tailwind CSS**, back‑end is **FastAPI** with Server‑Sent Events for streaming.

---

## 📂 Project structure

```text
rag-newsbot/
├── backend/            # FastAPI service
│   ├── main.py         # API + SSE streaming
│   ├── rag_utils.py    # embeddings, vector, redis helpers
│   ├── ingest.py       # CLI to pull + chunk RSS articles
│   ├── requirements.txt
│   └── .env.example
├── frontend/           # Vite + React chat UI
│   ├── src/App.jsx
│   ├── src/api.js
│   ├── index.html
│   ├── tailwind.config.cjs
│   └── …
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Stack choices

| Concern  | Tool              | Why                                   |
| -------- | ----------------- | ------------------------------------- |
| Embeds   | **Jina v2**       | Free‑tier key, strong English perf    |
| Vector   | **Qdrant**        | Fast HNSW + filtering, Docker‑friendly|
| LLM      | **GPT‑4o‑mini**   | High quality, streams tokens          |
| API      | **FastAPI**       | Async & auto‑docs                     |
| Cache    | **Redis**         | Session chat history                  |
| Frontend | **React + Vite**  | Fast dev HMR, Tailwind utilities      |

---

## 🏃‍♂️ Quick start

```bash
git clone https://github.com/<you>/rag-newsbot.git
cd rag-newsbot
cp backend/.env.example backend/.env  # add your keys
docker compose up -d qdrant redis
cd backend && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python ingest.py "https://news.google.com/rss/search?q=Apple"
python -m uvicorn main:app --reload --port 8000
cd ../frontend && npm install && npm run dev
```

See `http://localhost:5173` for the chat UI and `http://localhost:8000/docs` for the API docs.

---

## 📜 License

MIT
