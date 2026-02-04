#!/usr/bin/env python3
"""
Jarvis AI Assistant - Automated Setup Script
This script helps users set up their Jarvis AI Assistant with proper configuration.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header():
    print(f"""
{Colors.BLUE}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                    🤖 JARVIS AI ASSISTANT                    ║
║                     Automated Setup Script                   ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
""")

def print_step(step, description):
    print(f"{Colors.BOLD}Step {step}:{Colors.END} {description}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python 3.8+ required. You have Python {version.major}.{version.minor}")
        return False
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_requirements():
    """Install Python requirements"""
    try:
        print("Installing Python dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print_success("Python dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install requirements: {e}")
        return False

def check_ollama():
    """Check if Ollama is installed"""
    if shutil.which("ollama") is None:
        print_warning("Ollama not found in PATH")
        print(f"{Colors.YELLOW}Please install Ollama:{Colors.END}")
        print("1. Go to https://ollama.ai/")
        print("2. Download and install Ollama")
        print("3. Run: ollama pull llama2")
        print("4. Re-run this setup script")
        return False
    
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"Ollama found: {result.stdout.strip()}")
            return True
    except Exception:
        pass
    
    print_error("Ollama installation issue")
    return False

def check_ollama_model():
    """Check if llama2 model is available"""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if "llama2" in result.stdout:
            print_success("LLaMA2 model found")
            return True
        else:
            print_warning("LLaMA2 model not found")
            print("Downloading LLaMA2 model (this may take a while)...")
            subprocess.run(["ollama", "pull", "llama2"], check=True)
            print_success("LLaMA2 model downloaded")
            return True
    except subprocess.CalledProcessError:
        print_error("Failed to download LLaMA2 model")
        return False

def setup_environment():
    """Set up environment configuration"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print_warning(".env file already exists")
        response = input("Do you want to reconfigure it? (y/N): ").lower()
        if response != 'y':
            print("Keeping existing .env file")
            return True
    
    if not env_example.exists():
        print_error(".env.example not found")
        return False
    
    # Copy example to .env
    shutil.copy(env_example, env_file)
    print_success("Created .env file from template")
    
    # Configure Pinecone (optional)
    print(f"\n{Colors.BOLD}Pinecone Configuration (Optional):{Colors.END}")
    print("Pinecone provides persistent memory for conversations.")
    print("You can skip this and the assistant will work with limited memory.")
    
    use_pinecone = input("Do you want to configure Pinecone? (y/N): ").lower()
    
    if use_pinecone == 'y':
        print("\nTo get a Pinecone API key:")
        print("1. Go to https://www.pinecone.io/")
        print("2. Sign up for a free account")
        print("3. Create a new project")
        print("4. Copy your API key from the dashboard")
        
        api_key = input("\nEnter your Pinecone API key (or press Enter to skip): ").strip()
        
        if api_key:
            index_name = input("Enter index name (default: jarvis-knowledge): ").strip()
            if not index_name:
                index_name = "jarvis-knowledge"
            
            # Update .env file
            with open(env_file, 'r') as f:
                content = f.read()
            
            content = content.replace("your_pinecone_api_key_here", api_key)
            content = content.replace("jarvis-knowledge", index_name)
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print_success("Pinecone configuration saved")
        else:
            print_warning("Skipping Pinecone configuration")
    else:
        print_warning("Skipping Pinecone configuration")
    
    return True

def test_setup():
    """Test if the setup is working"""
    print(f"\n{Colors.BOLD}Testing setup...{Colors.END}")
    
    try:
        # Test imports
        import fastapi
        import uvicorn
        from sentence_transformers import SentenceTransformer
        print_success("All required packages can be imported")
        
        # Test if services can be initialized
        sys.path.append('.')
        from services.vector_service import VectorService
        from services.llm_service import LLMService
        
        print("Initializing services...")
        vector_service = VectorService()
        llm_service = LLMService()
        
        print_success("Services initialized successfully")
        return True
        
    except Exception as e:
        print_error(f"Setup test failed: {e}")
        return False

def main():
    print_header()
    
    print_step(1, "Checking Python version")
    if not check_python_version():
        sys.exit(1)
    
    print_step(2, "Installing Python dependencies")
    if not install_requirements():
        sys.exit(1)
    
    print_step(3, "Checking Ollama installation")
    if not check_ollama():
        sys.exit(1)
    
    print_step(4, "Checking LLaMA2 model")
    if not check_ollama_model():
        sys.exit(1)
    
    print_step(5, "Setting up environment configuration")
    if not setup_environment():
        sys.exit(1)
    
    print_step(6, "Testing setup")
    if not test_setup():
        print_warning("Setup test failed, but you can still try running the application")
    
    print(f"""
{Colors.GREEN}{Colors.BOLD}
🎉 Setup Complete! 🎉
{Colors.END}

Your Jarvis AI Assistant is ready to use!

{Colors.BOLD}To start the assistant:{Colors.END}
    python app.py

{Colors.BOLD}Then open your browser to:{Colors.END}
    http://localhost:8000

{Colors.BOLD}Need help?{Colors.END}
    - Check SETUP_GUIDE.md for detailed instructions
    - Visit: https://github.com/Pratiklakkundi/Jarvis-Self-ai-chatbot

{Colors.YELLOW}Note: If you skipped Pinecone configuration, the assistant will work
but won't remember conversations between sessions.{Colors.END}
""")

if __name__ == "__main__":
    main()