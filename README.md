# 🤖 Jarvis - Personal AI Assistant

A powerful self-hosted AI assistant powered by Ollama (LLaMA) with vector database storage for intelligent conversations and knowledge retention.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 🧠 **Local LLM**: Powered by Ollama with LLaMA2 model (completely offline)
- 🔍 **Vector Search**: Pinecone integration for intelligent context retrieval
- 💬 **Web Interface**: Clean, responsive chat interface
- 🔒 **Privacy First**: All conversations can run completely locally
- 📚 **Knowledge Base**: Add and search through your own documents
- ⚡ **Fast Setup**: Automated setup script for easy installation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Option 1: Automated Setup (Recommended)
```bash
git clone https://github.com/Pratiklakkundi/Jarvis-Self-ai-chatbot.git
cd Jarvis-Self-ai-chatbot
python setup_assistant.py
```

### Option 2: Manual Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/Pratiklakkundi/Jarvis-Self-ai-chatbot.git
   cd Jarvis-Self-ai-chatbot
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Ollama**
   - Download from [ollama.ai](https://ollama.ai/)
   - Install and run: `ollama pull llama2`

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys (optional for Pinecone)
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   - Go to: http://localhost:8000

## 🔧 Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```env
# Ollama Configuration (Required)
OLLAMA_MODEL=llama2

# Pinecone Configuration (Optional - for enhanced memory)
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=jarvis-knowledge
```

### Getting API Keys

#### Pinecone (Optional - for persistent memory)
1. Sign up at [pinecone.io](https://www.pinecone.io/)
2. Create a new project
3. Get your API key from the dashboard
4. Add it to your `.env` file

**Note**: The assistant works without Pinecone, but won't remember conversations between sessions.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │────│   FastAPI App   │────│   Ollama LLM    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                │
                       ┌─────────────────┐
                       │  Vector Store   │
                       │   (Pinecone)    │
                       └─────────────────┘
```

- **Frontend**: Simple HTML/CSS/JS chat interface
- **Backend**: FastAPI with async support
- **LLM**: Local Ollama server with LLaMA2
- **Vector DB**: Pinecone for semantic search and memory
- **Embeddings**: SentenceTransformers for text vectorization

## 📖 Usage

### Basic Chat
1. Open http://localhost:8000
2. Type your message and press Enter
3. Jarvis will respond using the local LLaMA model

### Adding Knowledge
Send a POST request to `/knowledge`:
```bash
curl -X POST "http://localhost:8000/knowledge" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your knowledge here", "source": "manual"}'
```

### API Endpoints
- `GET /` - Web interface
- `POST /chat` - Send message to AI
- `POST /knowledge` - Add knowledge to vector store

## 🛠️ Development

### Project Structure
```
jarvis-ai-assistant/
├── app.py                 # Main FastAPI application
├── services/
│   ├── llm_service.py     # Ollama integration
│   └── vector_service.py  # Pinecone integration
├── requirements.txt       # Python dependencies
├── setup_assistant.py     # Automated setup script
├── .env.example          # Environment template
└── README.md             # This file
```

### Running in Development
```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

## 🔍 Troubleshooting

### Common Issues

**Ollama not found**
- Make sure Ollama is installed and in your PATH
- Run `ollama --version` to verify installation

**Pinecone connection failed**
- Check your API key in `.env`
- Verify your Pinecone project is active
- The app works without Pinecone (limited memory)

**Port already in use**
- Change the port in `app.py`: `uvicorn.run(app, host="127.0.0.1", port=8001)`

### Getting Help
1. Check the [Setup Guide](SETUP_GUIDE.md) for detailed instructions
2. Run the setup script: `python setup_assistant.py`
3. Open an issue on GitHub

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for local LLM hosting
- [Pinecone](https://www.pinecone.io/) for vector database
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [SentenceTransformers](https://www.sbert.net/) for embeddings

---

**⭐ If you find this project helpful, please give it a star!**