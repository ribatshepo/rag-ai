"""Storage and retrieval interfaces."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
import numpy as np


class IVectorStore(ABC):
    """Abstract base class for vector database operations.
    
    Defines the interface for storing and retrieving vector embeddings
    with associated metadata.
    """
    
    __slots__ = ()
    
    @abstractmethod
    async def store(
        self, 
        embeddings: List["Embedding"]
    ) -> List[str]:
        """Store embeddings in the vector database.
        
        Args:
            embeddings: List of embeddings to store
            
        Returns:
            List[str]: List of stored document IDs
        """
        pass
    
    @abstractmethod
    async def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[str, float]]:
        """Search for similar embeddings.
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            filters: Optional search filters
            
        Returns:
            List[Tuple[str, float]]: List of (doc_id, similarity_score)
        """
        pass
    
    @abstractmethod
    async def delete(self, doc_ids: List[str]) -> bool:
        """Delete embeddings by document IDs.
        
        Args:
            doc_ids: List of document IDs to delete
            
        Returns:
            bool: True if deletion was successful
        """
        pass
    
    @abstractmethod
    async def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics.
        
        Returns:
            Dict[str, Any]: Store statistics
        """
        pass


class IEmbeddingGenerator(ABC):
    """Abstract base class for text embedding generation."""
    
    __slots__ = ()
    
    @abstractmethod
    async def generate(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for text inputs.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List[np.ndarray]: Generated embeddings
        """
        pass
    
    @property
    @abstractmethod
    def embedding_dimension(self) -> int:
        """Get the embedding vector dimension."""
        pass


class IRetrievalStrategy(ABC):
    """Abstract base class for document retrieval strategies."""
    
    __slots__ = ()
    
    @abstractmethod
    async def retrieve(
        self,
        query: "Query",
        top_k: int = 10
    ) -> List["Document"]:
        """Retrieve relevant documents for a query.
        
        Args:
            query: User query
            top_k: Number of documents to retrieve
            
        Returns:
            List[Document]: Retrieved documents
        """
        pass