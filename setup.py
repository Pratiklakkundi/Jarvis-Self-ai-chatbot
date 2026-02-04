#!/usr/bin/env python3
"""
Setup script for Jarvis AI Assistant
"""

import os
import subprocess
import sys

def install_ollama():
    """Install Ollama if not present"""
    print("🔧 Setting up Ollama...")
    
    # Check if Ollama is installed
    try:
        subprocess.run(["ollama", "--version"], check=True, capture_output=True)
        print("✅ Ollama is already installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Ollama not found. Please install it from: https://ollama.ai/")
        print("After installation, run: ollama pull llama2")
        return False
    
    # Check if model is available
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if "llama2" not in result.stdout:
            print("📥 Downloading LLaMA2 model...")
            subprocess.run(["ollama", "pull", "llama2"], check=True)
        print("✅ LLaMA2 model ready")
    except subprocess.CalledProcessError:
        print("❌ Failed to setup LLaMA2 model")
        return False
    
    return True

def setup_environment():
    """Setup environment file"""
    if not os.path.exists(".env"):
        print("📝 Creating .env file...")
        with open(".env", "w") as f:
            f.write("# Copy from .env.example and fill in your values\n")
            f.write("PINECONE_API_KEY=your_pinecone_api_key_here\n")
            f.write("PINECONE_ENVIRONMENT=your_pinecone_environment\n")
            f.write("PINECONE_INDEX_NAME=jarvis-knowledge\n")
            f.write("OLLAMA_MODEL=llama2\n")
        print("✅ Created .env file - please configure your Pinecone credentials")
    else:
        print("✅ .env file already exists")

def main():
    print("🚀 Setting up Jarvis AI Assistant...")
    
    # Install Python dependencies
    print("📦 Installing Python dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Setup Ollama
    if not install_ollama():
        print("⚠️  Ollama setup incomplete. Please install manually.")
    
    # Setup environment
    setup_environment()
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Configure your Pinecone API key in .env file")
    print("2. Make sure Ollama is running: ollama serve")
    print("3. Start the application: python app.py")
    print("4. Open http://localhost:8000 in your browser")

if __name__ == "__main__":
    main()