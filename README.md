# Personal AI Assistant (Jarvis)

A self-hosted AI assistant powered by LLaMA, with vector database storage and conversational interface.

## Features
- Self-hosted LLM integration (LLaMA)
- Vector database for knowledge storage (Pinecone)
- Conversational chatbot UI
- Context-aware responses

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment variables in `.env`
3. Run the application: `python app.py`

## Architecture
- **Backend**: FastAPI with LLM integration
- **Vector DB**: Pinecone for knowledge storage
- **Frontend**: Simple web interface
- **LLM**: Local LLaMA model via Ollama