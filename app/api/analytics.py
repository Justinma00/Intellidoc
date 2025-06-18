from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, auth
from ..database import get_db
from ..services.vector_store import VectorStore

router = APIRouter()
vector_store = VectorStore()

@router.get("/dashboard")
def get_dashboard_stats(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Get document statistics
    total_docs = db.query(models.Document).filter(
        models.Document.owner_id == current_user.id
    ).count()
    
    processed_docs = db.query(models.Document).filter(
        models.Document.owner_id == current_user.id,
        models.Document.processed_at.isnot(None)
    ).count()
    
    # Category distribution
    category_stats = db.query(
        models.Document.category,
        func.count(models.Document.id).label('count')
    ).filter(
        models.Document.owner_id == current_user.id
    ).group_by(models.Document.category).all()
    
    # Recent documents
    recent_docs = db.query(models.Document).filter(
        models.Document.owner_id == current_user.id
    ).order_by(models.Document.created_at.desc()).limit(5).all()
    
    # Vector store stats
    vector_stats = vector_store.get_collection_stats()
    
    return {
        "total_documents": total_docs,
        "processed_documents": processed_docs,
        "processing_rate": (processed_docs / max(total_docs, 1)) * 100,
        "category_distribution": [
            {"category": cat, "count": count} for cat, count in category_stats
        ],
        "recent_documents": [
            {
                "id": doc.id,
                "filename": doc.original_filename,
                "category": doc.category,
                "created_at": doc.created_at
            } for doc in recent_docs
        ],
        "vector_store_stats": vector_stats
    }