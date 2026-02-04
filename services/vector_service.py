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
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize Pinecone only if API key is provided
        if self.api_key:
            try:
                self.pc = Pinecone(api_key=self.api_key)
                
                # Create index if it doesn't exist
                existing_indexes = [index.name for index in self.pc.list_indexes()]
                if self.index_name not in existing_indexes:
                    self.pc.create_index(
                        name=self.index_name,
                        dimension=384,  # all-MiniLM-L6-v2 dimension
                        metric="cosine",
                        spec=ServerlessSpec(cloud="aws", region="us-east-1")
                    )
                
                self.index = self.pc.Index(self.index_name)
                print("✅ Pinecone vector database connected successfully")
            except Exception as e:
                print(f"❌ Pinecone connection failed: {str(e)}")
                self.index = None
        else:
            self.index = None
            print("⚠️  Pinecone not configured. Vector search will be limited.")
    
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