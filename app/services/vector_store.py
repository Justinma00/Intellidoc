from typing import List, Dict, Any, Optional, Tuple
import os
from ..config import settings

class VectorStore:
    def __init__(self) -> None:
        # Try chromadb; if unavailable, fall back to a minimal in-memory store
        self._use_memory = False
        try:
            import chromadb  # type: ignore
            from chromadb.config import Settings  # type: ignore

            fast_init = os.getenv("INTELLIDOC_FAST_INIT") == "1"
            if fast_init:
                self.client = chromadb.Client(Settings(anonymized_telemetry=False))
            else:
                self.client = chromadb.PersistentClient(
                    path=settings.chroma_persist_dir,
                    settings=Settings(anonymized_telemetry=False),
                )
            self.collection = self.client.get_or_create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"},
            )
        except Exception:
            # In-memory fallback
            self._use_memory = True
            self._memory_docs: Dict[str, Tuple[str, List[float], Dict[str, Any]]] = {}
    
    def add_document(self, doc_id: str, text: str, embeddings: List[float], metadata: Dict[str, Any]) -> bool:
        """Add document to vector store."""
        try:
            chunks = self._split_text(text)
            if self._use_memory:
                for i, chunk in enumerate(chunks):
                    chunk_id = f"{doc_id}_chunk_{i}"
                    self._memory_docs[chunk_id] = (chunk, embeddings, {**metadata, "chunk_index": i, "parent_doc_id": doc_id})
                return True
            # chromadb path
            ids = []
            texts = []
            embeds = []
            metas = []
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_id}_chunk_{i}"
                ids.append(chunk_id)
                texts.append(chunk)
                embeds.append(embeddings)
                metas.append({**metadata, "chunk_index": i, "parent_doc_id": doc_id})
            self.collection.add(ids=ids, documents=texts, embeddings=embeds, metadatas=metas)
            return True
        except Exception as e:
            print(f"Error adding document to vector store: {e}")
            return False
    
    def search_documents(self, query_embeddings: List[float], n_results: int = 10, where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        try:
            if self._use_memory:
                def cosine(a: List[float], b: List[float]) -> float:
                    import math
                    if not a or not b or len(a) != len(b):
                        return 0.0
                    dot = sum(x * y for x, y in zip(a, b))
                    na = math.sqrt(sum(x * x for x in a))
                    nb = math.sqrt(sum(y * y for y in b))
                    return dot / (na * nb) if na and nb else 0.0

                matches = []
                for chunk_id, (chunk_text, emb, meta) in self._memory_docs.items():
                    if where and any(k in meta and meta[k] != v for k, v in where.items()):
                        continue
                    score = cosine(query_embeddings, emb)
                    matches.append({"id": chunk_id, "document": chunk_text, "distance": 1 - score, "metadata": meta})
                matches.sort(key=lambda m: m["distance"])
                return matches[:n_results]

            # chromadb path
            results = self.collection.query(query_embeddings=[query_embeddings], n_results=n_results, where=where)
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
        """Delete document from vector store."""
        try:
            if self._use_memory:
                to_delete = [k for k, v in self._memory_docs.items() if v[2].get("parent_doc_id") == doc_id]
                for k in to_delete:
                    self._memory_docs.pop(k, None)
                return True
            results = self.collection.get(where={"parent_doc_id": doc_id})
            if results['ids']:
                self.collection.delete(ids=results['ids'])
            return True
        except Exception as e:
            print(f"Error deleting document from vector store: {e}")
            return False
    
    def _split_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into chunks with overlap."""
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
        """Get statistics about the collection."""
        try:
            if self._use_memory:
                return {"total_documents": len(self._memory_docs), "collection_name": "memory"}
            count = self.collection.count()
            return {"total_documents": count, "collection_name": self.collection.name}
        except Exception as e:
            return {"total_documents": 0, "error": str(e)}