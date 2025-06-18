import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from ..config import settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_document(self, doc_id: str, text: str, embeddings: List[float], 
                    metadata: Dict[str, Any]) -> bool:
        """Add document to vector store"""
        try:
            # Split text into chunks for better search
            chunks = self._split_text(text)
            
            ids = []
            texts = []
            embeds = []
            metas = []
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_id}_chunk_{i}"
                ids.append(chunk_id)
                texts.append(chunk)
                embeds.append(embeddings)  # Using same embedding for all chunks (simplified)
                metas.append({
                    **metadata,
                    "chunk_index": i,
                    "parent_doc_id": doc_id
                })
            
            self.collection.add(
                ids=ids,
                documents=texts,
                embeddings=embeds,
                metadatas=metas
            )
            return True
            
        except Exception as e:
            print(f"Error adding document to vector store: {e}")
            return False
    
    def search_documents(self, query_embeddings: List[float], 
                        n_results: int = 10, 
                        where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            results = self.collection.query(
                query_embeddings=[query_embeddings],
                n_results=n_results,
                where=where
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    "id": results['ids'][0][i],
                    "document": results['documents'][0][i],
                    "distance": results['distances'][0][i],
                    "metadata": results['metadatas'][0][i]
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"Error searching vector store: {e}")
            return []
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete document from vector store"""
        try:
            # Get all chunks for this document
            results = self.collection.get(
                where={"parent_doc_id": doc_id}
            )
            
            if results['ids']:
                self.collection.delete(ids=results['ids'])
            
            return True
            
        except Exception as e:
            print(f"Error deleting document from vector store: {e}")
            return False
    
    def _split_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into chunks with overlap"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings
                sentence_end = text.rfind('.', start, end)
                if sentence_end != -1 and sentence_end > start + chunk_size // 2:
                    end = sentence_end + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = max(start + chunk_size - overlap, end)
        
        return chunks
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": self.collection.name
            }
        except Exception as e:
            return {
                "total_documents": 0,
                "error": str(e)
            }