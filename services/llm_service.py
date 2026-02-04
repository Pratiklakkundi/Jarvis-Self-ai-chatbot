import ollama
import os
from typing import List, Dict

class LLMService:
    def __init__(self):
        self.model = os.getenv("OLLAMA_MODEL", "llama2")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.use_openai = bool(self.openai_api_key and self.openai_api_key != "your_openai_api_key_here")
        
        if self.use_openai:
            try:
                import openai
                self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
                print("✅ Using OpenAI API")
            except ImportError:
                print("❌ OpenAI package not installed. Install with: pip install openai")
                self.use_openai = False
        else:
            # Test Ollama connection
            try:
                print(f"🔄 Testing Ollama connection with model: {self.model}")
                # Test if Ollama is running and model is available
                response = ollama.generate(
                    model=self.model,
                    prompt="Hello",
                    options={"max_tokens": 1}
                )
                print(f"✅ Ollama connected successfully with {self.model} model")
            except Exception as e:
                print(f"❌ Ollama connection failed: {str(e)}")
                print("💡 Make sure Ollama is installed and running")
                print(f"💡 Run: ollama pull {self.model}")
                print("💡 Or add OPENAI_API_KEY to your .env file to use OpenAI instead")
        
    async def generate_response(self, query: str, context: List[Dict] = None) -> str:
        """Generate response using local LLaMA model via Ollama or OpenAI"""
        try:
            # Build context from retrieved documents
            context_text = ""
            if context:
                context_text = "\n".join([doc.get("text", "") for doc in context[:3]])
                context_text = f"Context information:\n{context_text}\n\n"
            
            # Create prompt
            prompt = f"""{context_text}User question: {query}

Please provide a helpful and accurate response based on the context provided (if any) and your knowledge. Be conversational and friendly."""

            if self.use_openai:
                # Use OpenAI API
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                return response.choices[0].message.content
            else:
                # Use Ollama
                response = ollama.generate(
                    model=self.model,
                    prompt=prompt,
                    options={
                        "temperature": 0.7,
                        "max_tokens": 500
                    }
                )
                return response['response']
            
        except Exception as e:
            if self.use_openai:
                return f"I'm sorry, I encountered an error with OpenAI: {str(e)}. Please check your API key."
            else:
                return f"I'm sorry, I encountered an error: {str(e)}. Please make sure Ollama is running with the {self.model} model, or add an OpenAI API key to use GPT instead."