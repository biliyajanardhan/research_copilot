# 🧠 Research Copilot – Agentic AI Paper Fetcher & Analyzer

Research Copilot is an **Agentic AI-powered web application** that fetches, analyzes, and summarizes research papers using **RAG (Retrieval-Augmented Generation)**.  
It provides a clean UI, real-time streaming responses, and modular AI agents for scalable research workflows.

---

## 🚀 Features

- 🔍 Search and fetch academic research papers
- 📄 Save and manage paper URLs
- 🧠 Agent-based architecture (Planner, Research, RAG, Answer agents)
- 📚 RAG pipeline with vector search
- ⚡ Real-time streaming responses (SSE)
- 🌐 Web UI using FastAPI + Jinja2
- 🔐 Secure environment-based configuration
- ☁️ Azure-ready architecture

---

## 🏗️ Project Architecture




---

## 🧠 Agentic Design

The system follows an **agent orchestration model**:

- **MasterAgent** – Coordinates the entire workflow
- **ResearchAgent** – Fetches and stores papers
- **RAG Agent** – Handles document retrieval and context building
- **LLM Answer Agent** – Generates final responses

Each agent is **loosely coupled**, making the system easy to extend.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML + Jinja2 + JavaScript
- **AI / LLM**: Azure OpenAI
- **Search**: Azure Cognitive Search
- **Storage**: Azure Blob Storage
- **Vector Store**: (Configurable – FAISS / Azure / Qdrant)
- **Streaming**: Server-Sent Events (SSE)

---

## 🔐 Environment Setup

### 1️⃣ Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
