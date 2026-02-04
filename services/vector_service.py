from pinecone import Pinecone, ServerlessSpec
import os
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import uuid

class VectorService:
    def __init__(self):
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "jarvis-knowledge")
        
        # Initialize embedding model
        print("🔄 Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Embedding model loaded successfully")
        
        # Initialize Pinecone only if API key is provided and valid
        if self.api_key and self.api_key != "your_pinecone_api_key_here":
            try:
                print("🔄 Connecting to Pinecone...")
                self.pc = Pinecone(api_key=self.api_key)
                
                # Test connection by listing indexes
                existing_indexes = [index.name for index in self.pc.list_indexes()]
                
                # Create index if it doesn't exist
                if self.index_name not in existing_indexes:
                    print(f"🔄 Creating Pinecone index: {self.index_name}")
                    self.pc.create_index(
                        name=self.index_name,
                        dimension=384,  # all-MiniLM-L6-v2 dimension
                        metric="cosine",
                        spec=ServerlessSpec(cloud="aws", region="us-east-1")
                    )
                    print(f"✅ Created Pinecone index: {self.index_name}")
                else:
                    print(f"✅ Using existing Pinecone index: {self.index_name}")
                
                self.index = self.pc.Index(self.index_name)
                print("✅ Pinecone vector database connected successfully")
                
            except Exception as e:
                print(f"❌ Pinecone connection failed: {str(e)}")
                print("💡 Tip: Check your API key in the .env file")
                print("💡 Get a free API key at: https://www.pinecone.io/")
                self.index = None
        else:
            self.index = None
            if not self.api_key:
                print("⚠️  No Pinecone API key found in environment")
            else:
                print("⚠️  Please update PINECONE_API_KEY in your .env file")
            print("💡 The assistant will work without Pinecone but won't remember conversations")
            print("💡 Run 'python setup_assistant.py' for guided setup")
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text"""
        return self.embedding_model.encode(text).tolist()
    
    async def add_document(self, text: str, metadata: Dict = None) -> str:
        """Add document to vector database"""
        if not self.index:
            return "Vector database not configured"
            
        try:
            # Generate embedding
            embedding = self._generate_embedding(text)
            
            # Create unique ID
            doc_id = str(uuid.uuid4())
            
            # Prepare metadata
            if metadata is None:
                metadata = {}
            metadata["text"] = text
            
            # Upsert to Pinecone
            self.index.upsert([(doc_id, embedding, metadata)])
            
            return doc_id
            
        except Exception as e:
            raise Exception(f"Error adding document: {str(e)}")
    
    async def search_similar(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for similar documents"""
        if not self.index:
            # Return empty context if no vector DB
            return []
            
        try:
            # Generate query embedding
            query_embedding = self._generate_embedding(query)
            
            # Search in Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Format results
            documents = []
            for match in results.matches:
                documents.append({
                    "text": match.metadata.get("text", ""),
                    "source": match.metadata.get("source", "unknown"),
                    "score": match.score
                })
            
            return documents
            
        except Exception as e:
            print(f"Error searching documents: {str(e)}")
            return []