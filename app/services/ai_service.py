import os
from typing import List, Dict, Any
from ..config import settings

class AIService:
    def __init__(self) -> None:
        # Determine device if torch is available, else default to CPU
        try:
            import torch  # type: ignore

            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        except Exception:
            self.device = "cpu"
        self.models: Dict[str, Any] = {}
        self.use_api: bool = False
        # Allow tests and constrained environments to skip heavyweight model init
        fast_init = os.getenv("INTELLIDOC_FAST_INIT") == "1"
        if not fast_init:
            self.setup_models()
        else:
            self.use_api = True
        
    def setup_models(self) -> None:
        """Initialize local AI models. Falls back to API-backed stubs on failure."""
        try:
            from transformers import pipeline  # type: ignore
            from sentence_transformers import SentenceTransformer  # type: ignore
            import torch  # type: ignore

            # Text classification
            self.models['classifier'] = pipeline(
                "text-classification",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=0 if self.device == "cuda" else -1
            )
            
            # Question answering
            self.models['qa'] = pipeline(
                "question-answering",
                model="deepset/roberta-base-squad2",
                device=0 if self.device == "cuda" else -1
            )
            
            # Summarization
            self.models['summarizer'] = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=0 if self.device == "cuda" else -1
            )
            
            # Sentence embeddings
            self.models['embedder'] = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Translation
            # Translator is optional; only initialize when API key/model available
            
        except Exception as e:
            print(f"Error setting up models: {e}")
            # Fallback to API-based models
            self.use_api = True
    
    def classify_document(self, text: str) -> Dict[str, Any]:
        """Classify document into categories using simple keyword heuristics."""
        try:
            # Define document categories
            categories = [
                "contract", "invoice", "legal", "financial", 
                "technical", "medical", "academic", "other"
            ]
            
            # Simple keyword-based classification for demo
            text_lower = text.lower()
            scores = {}
            
            keywords = {
                "contract": ["agreement", "contract", "terms", "conditions"],
                "invoice": ["invoice", "payment", "amount", "due"],
                "legal": ["legal", "court", "law", "attorney"],
                "financial": ["financial", "revenue", "profit", "loss"],
                "technical": ["technical", "specification", "requirements"],
                "medical": ["medical", "patient", "diagnosis", "treatment"],
                "academic": ["research", "study", "analysis", "paper"]
            }
            
            for category, words in keywords.items():
                score = sum(1 for word in words if word in text_lower)
                scores[category] = score / len(words)
            
            # Get best category
            best_category = max(scores, key=scores.get)
            confidence = scores[best_category]
            
            return {
                "category": best_category,
                "confidence": confidence,
                "all_scores": scores
            }
            
        except Exception as e:
            return {
                "category": "other",
                "confidence": 0.5,
                "error": str(e)
            }
    
    def answer_question(self, question: str, context: str) -> Dict[str, Any]:
        """Answer questions about document content using a QA model or fallback heuristic."""
        try:
            if 'qa' in self.models:
                result = self.models['qa'](question=question, context=context)
                return {
                    "answer": result['answer'],
                    "confidence": result['score'],
                    "start": result['start'],
                    "end": result['end']
                }
            else:
                # Fallback simple search
                context_lower = context.lower()
                question_lower = question.lower()
                
                # Simple keyword matching
                question_words = question_lower.split()
                sentences = context.split('.')
                
                best_sentence = ""
                best_score = 0
                
                for sentence in sentences:
                    score = sum(1 for word in question_words if word in sentence.lower())
                    if score > best_score:
                        best_score = score
                        best_sentence = sentence.strip()
                
                return {
                    "answer": best_sentence,
                    "confidence": min(best_score / len(question_words), 1.0),
                    "start": 0,
                    "end": len(best_sentence)
                }
                
        except Exception as e:
            return {
                "answer": "Unable to answer question",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def summarize_text(self, text: str, max_length: int = 150) -> Dict[str, Any]:
        """Generate text summary via abstractive model or simple extractive fallback."""
        try:
            if len(text) < 100:
                return {
                    "summary": text,
                    "confidence": 1.0
                }
            
            if 'summarizer' in self.models:
                result = self.models['summarizer'](
                    text, 
                    max_length=max_length, 
                    min_length=30,
                    do_sample=False
                )
                return {
                    "summary": result[0]['summary_text'],
                    "confidence": 0.8
                }
            else:
                # Simple extractive summarization
                sentences = text.split('.')
                if len(sentences) <= 3:
                    return {
                        "summary": text,
                        "confidence": 1.0
                    }
                
                # Take first and last sentences
                summary = f"{sentences[0]}. {sentences[-2]}."
                return {
                    "summary": summary,
                    "confidence": 0.6
                }
                
        except Exception as e:
            return {
                "summary": text[:200] + "..." if len(text) > 200 else text,
                "confidence": 0.5,
                "error": str(e)
            }
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts."""
        try:
            if 'embedder' in self.models:
                embeddings = self.models['embedder'].encode(texts)
                return embeddings.tolist()
            else:
                # Fallback: simple hash-based embeddings
                import hashlib
                embeddings = []
                for text in texts:
                    # Simple hash-based embedding (not semantic)
                    hash_obj = hashlib.md5(text.encode())
                    hash_int = int(hash_obj.hexdigest(), 16)
                    # Convert to fixed-size vector
                    embedding = [(hash_int >> i) & 1 for i in range(128)]
                    embeddings.append(embedding)
                return embeddings
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return [[0.0] * 128 for _ in texts]
    
    def translate_text(self, text: str, target_lang: str = "es") -> Dict[str, Any]:
        """Translate text to target language. Optional; falls back to passthrough."""
        try:
            if 'translator' in self.models and target_lang == "es":
                result = self.models['translator'](text)
                return {
                    "translated_text": result[0]['translation_text'],
                    "confidence": 0.8,
                    "target_language": target_lang,
                }
            return {
                "translated_text": text,
                "confidence": 0.5,
                "target_language": "en",
                "note": "Translation not available for this language",
            }
        except Exception as e:
            return {"translated_text": text, "confidence": 0.0, "error": str(e)}