from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from services.llm_service import LLMService
from services.vector_service import VectorService

load_dotenv()

app = FastAPI(title="Personal AI Assistant (Jarvis)")

# Initialize services
llm_service = LLMService()
vector_service = VectorService()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    sources: list = []

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Search for relevant context
        context = await vector_service.search_similar(request.message)
        
        # Generate response using LLM
        response = await llm_service.generate_response(request.message, context)
        
        return ChatResponse(
            response=response,
            sources=[doc.get("source", "") for doc in context]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/knowledge")
async def add_knowledge(text: str, source: str = "user_input"):
    try:
        await vector_service.add_document(text, {"source": source})
        return {"message": "Knowledge added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jarvis - Personal AI Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .chat-container { border: 1px solid #ddd; height: 400px; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
            .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
            .user { background-color: #e3f2fd; text-align: right; }
            .assistant { background-color: #f5f5f5; }
            input[type="text"] { width: 70%; padding: 10px; }
            button { padding: 10px 20px; margin-left: 10px; }
        </style>
    </head>
    <body>
        <h1>🤖 Jarvis - Personal AI Assistant</h1>
        <div id="chat-container" class="chat-container"></div>
        <input type="text" id="message-input" placeholder="Ask me anything..." onkeypress="handleKeyPress(event)">
        <button onclick="sendMessage()">Send</button>
        
        <script>
            async function sendMessage() {
                const input = document.getElementById('message-input');
                const message = input.value.trim();
                if (!message) return;
                
                addMessage(message, 'user');
                input.value = '';
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message })
                    });
                    const data = await response.json();
                    addMessage(data.response, 'assistant');
                } catch (error) {
                    addMessage('Sorry, I encountered an error.', 'assistant');
                }
            }
            
            function addMessage(text, sender) {
                const container = document.getElementById('chat-container');
                const div = document.createElement('div');
                div.className = `message ${sender}`;
                div.textContent = text;
                container.appendChild(div);
                container.scrollTop = container.scrollHeight;
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') sendMessage();
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)