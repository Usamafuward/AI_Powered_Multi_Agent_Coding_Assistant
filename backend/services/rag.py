import logging
import os
import json
from typing import List, Dict, Any, Optional
import faiss
import numpy as np
from openai import OpenAI
import pickle

from backend.config import get_settings

# Configure logging
logger = logging.getLogger(__name__)

class RAGService:
    """Service for Retrieval-Augmented Generation (RAG)."""
    
    def __init__(self, vector_db_path: str):
        """
        Initialize the RAG service.
        
        Args:
            vector_db_path: Path to the vector database
        """
        self.vector_db_path = vector_db_path
        self.settings = get_settings()
        self.client = OpenAI(api_key=self.settings.openai_api_key)
        
        # Initialize or load the vector index and documents
        self.index, self.documents = self._initialize_vector_store()
        
        logger.info("RAG Service initialized")
    
    def _initialize_vector_store(self):
        """Initialize or load the vector store."""
        index_path = os.path.join(self.vector_db_path, "index.faiss")
        docs_path = os.path.join(self.vector_db_path, "documents.pkl")
        
        if os.path.exists(index_path) and os.path.exists(docs_path):
            # Load existing index and documents
            logger.info("Loading existing vector store")
            index = faiss.read_index(index_path)
            with open(docs_path, 'rb') as f:
                documents = pickle.load(f)
        else:
            # Create a new index and empty documents list
            logger.info("Creating new vector store")
            os.makedirs(self.vector_db_path, exist_ok=True)
            
            # Create a simple L2 index
            dimension = 1536  # OpenAI's embedding dimension
            index = faiss.IndexFlatL2(dimension)
            documents = []
            
            # Save the empty index and documents
            faiss.write_index(index, index_path)
            with open(docs_path, 'wb') as f:
                pickle.dump(documents, f)
        
        return index, documents
    
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding for the given text."""
        response = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
    
    def add_document(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> int:
        """
        Add a document to the vector store.
        
        Args:
            content: Document content
            metadata: Optional metadata for the document
            
        Returns:
            Document ID
        """
        # Get embedding
        embedding = self._get_embedding(content)
        
        # Add to index
        embedding_np = np.array([embedding], dtype=np.float32)
        self.index.add(embedding_np)
        
        # Add to documents
        doc_id = len(self.documents)
        self.documents.append({
            "id": doc_id,
            "content": content,
            "metadata": metadata or {}
        })
        
        # Save updates
        faiss.write_index(self.index, os.path.join(self.vector_db_path, "index.faiss"))
        with open(os.path.join(self.vector_db_path, "documents.pkl"), 'wb') as f:
            pickle.dump(self.documents, f)
        
        logger.info(f"Added document with ID {doc_id}")
        return doc_id
    
    def retrieve(self, query: str, top_k: int = 5) -> str:
        """
        Retrieve relevant context for the query.
        
        Args:
            query: Query string
            top_k: Number of top results to return
            
        Returns:
            Concatenated relevant context
        """
        # If index is empty, return empty string
        if self.index.ntotal == 0:
            logger.info("Index is empty, returning empty context")
            return ""
        
        # Get query embedding
        query_embedding = self._get_embedding(query)
        query_embedding_np = np.array([query_embedding], dtype=np.float32)
        
        # Search the index
        top_k = min(top_k, self.index.ntotal)
        distances, indices = self.index.search(query_embedding_np, top_k)
        
        # Get the documents
        retrieved_docs = [self.documents[int(idx)] for idx in indices[0]]
        
        # Format the context
        context = "\n\n".join([f"Document {i+1}:\n{doc['content']}" 
                              for i, doc in enumerate(retrieved_docs)])
        
        logger.info(f"Retrieved {len(retrieved_docs)} documents for query: {query[:50]}...")
        return context
    
    def clear(self) -> None:
        """Clear the vector store."""
        # Create a new index
        dimension = 1536
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []
        
        # Save the empty index and documents
        faiss.write_index(self.index, os.path.join(self.vector_db_path, "index.faiss"))
        with open(os.path.join(self.vector_db_path, "documents.pkl"), 'wb') as f:
            pickle.dump(self.documents, f)
        
        logger.info("Cleared vector store")