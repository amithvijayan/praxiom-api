import os
from typing import List, Dict, Any
import uuid
import google.generativeai as genai
from pinecone import Pinecone, ServerlessSpec

# We will initialize this class lazily to ensure environment variables are loaded
class VectorMemoryVault:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        pc_api_key = os.environ.get("PINECONE_API_KEY")
        if not pc_api_key:
            raise ValueError("PINECONE_API_KEY environment variable not set")
            
        self.pc = Pinecone(api_key=pc_api_key)
        self.index_name = "praxiom-memory"
        
        # Ensure the index exists, if not, create it with 768 dimensions (for text-embedding-004)
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=768, 
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1' # Default serverless region
                )
            )
            
        self.index = self.pc.Index(self.index_name)

    def generate_embeddings(self, text: str) -> List[float]:
        """Generate 768-dimensional embeddings using Gemini."""
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document",
            title="ISTA Knowledge Base"
        )
        return result['embedding']

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split large text into overlapping chunks."""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
            
        return chunks

    def memorize_document(self, text: str, source_url: str = "Unknown", title: str = "Document"):
        """Chunk a document, embed it, and store it permanently in Pinecone."""
        chunks = self.chunk_text(text)
        
        vectors = []
        for i, chunk in enumerate(chunks):
            vector_id = f"{title.replace(' ', '_')}_chunk_{i}_{uuid.uuid4().hex[:8]}"
            embedding = self.generate_embeddings(chunk)
            
            # We store the raw text as metadata so we can read it later
            metadata = {
                "source": source_url,
                "title": title,
                "text": chunk
            }
            
            vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": metadata
            })
            
        # Upsert in batches of 100
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            self.index.upsert(vectors=vectors[i:i + batch_size])
            
        return len(chunks)

    def recall_facts(self, query: str, top_k: int = 3) -> str:
        """Search Pinecone for the most mathematically relevant facts."""
        query_embedding = genai.embed_content(
            model="models/text-embedding-004",
            content=query,
            task_type="retrieval_query",
        )['embedding']
        
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        if not results.matches:
            return ""
            
        # Combine the text from the top matches
        recalled_text = "--- RETRIEVED ISTA MEMORY VAULT KNOWLEDGE ---\n"
        for match in results.matches:
            score = match.score
            metadata = match.metadata
            recalled_text += f"Source: {metadata.get('title')} ({metadata.get('source')}) [Relevance: {score:.2f}]\n"
            recalled_text += f"Fact: {metadata.get('text')}\n\n"
            
        return recalled_text
