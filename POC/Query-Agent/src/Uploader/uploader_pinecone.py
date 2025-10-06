import sys
import os
from pathlib import Path
from abc import ABC, abstractmethod
from langchain_experimental.text_splitter import SemanticChunker
from sentence_transformers import SentenceTransformer
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone, ServerlessSpec

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent 
sys.path.insert(0, str(project_root))

from settings import GOOGLE_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME, PINECONE_REGION
from src.document_loader.local_loader import get_combined_text

class DocumentUploader(ABC):
    
    def __init__(self):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index_name = PINECONE_INDEX_NAME
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.semantic_chunker = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001", 
            google_api_key=GOOGLE_API_KEY
        )
    
    @abstractmethod
    def semantic_chunking(self, text: str):
        pass
    
    @abstractmethod
    def embed_chunks(self, chunks):
        pass
    
    def ensure_index(self):
        if not self.pc.has_index(self.index_name):
            self.pc.create_index(
                name=self.index_name,
                dimension=384,  # Dimension for all-MiniLM-L6-v2
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region=PINECONE_REGION or "us-east-1")
            )
        self.index = self.pc.Index(self.index_name)
    
    def upload_documents(self, documents_dir: str = "documents"):
        combined_text = get_combined_text(documents_dir)
        
        if not combined_text or "No readable content found" in combined_text:
            print("No content to upload")
            return

        self.ensure_index()

        chunks = self.semantic_chunking(combined_text)

        embeddings = self.embed_chunks(chunks)

        pinecone_vectors = []
        for i, (embedding, chunk) in enumerate(zip(embeddings, chunks)):
            vector_data = {
                "id": f"chunk_{i}",
                "values": embedding.tolist(),
                "metadata": {
                    "chunk_text": chunk.page_content,
                    "chunk_id": i,
                    "source": "documents_folder"
                }
            }
            pinecone_vectors.append(vector_data)

        self.index.upsert(vectors=pinecone_vectors)
        print(f" Uploaded {len(pinecone_vectors)} chunks to Pinecone index '{self.index_name}'")

class MyDocumentUploader(DocumentUploader):
    
    def semantic_chunking(self, text: str):
        text_splitter = SemanticChunker(
            self.semantic_chunker, 
            breakpoint_threshold_type="percentile"
        )
        chunks = text_splitter.create_documents([text])
        print(f"Created {len(chunks)} semantic chunks")
        return chunks
    
    def embed_chunks(self, chunks):
        chunk_texts = [chunk.page_content for chunk in chunks]
        embeddings = self.embedding_model.encode(chunk_texts, convert_to_numpy=True)
        print(f"🔗 Generated embeddings for {len(embeddings)} chunks")
        return embeddings

if __name__ == "__main__":
    uploader = MyDocumentUploader()
    uploader.upload_documents()