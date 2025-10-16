from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from . import models, schemas
from .auth import get_password_hash

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_documents(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Document]:
    return db.query(models.Document).filter(
        models.Document.owner_id == user_id
    ).order_by(desc(models.Document.created_at)).offset(skip).limit(limit).all()

def get_document(db: Session, document_id: int, user_id: int) -> Optional[models.Document]:
    return db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.owner_id == user_id
    ).first()

def create_document(db: Session, document: schemas.DocumentCreate, 
                   user_id: int, file_info: dict) -> models.Document:
    db_document = models.Document(
        **document.dict(),
        **file_info,
        owner_id=user_id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def update_document(db: Session, document_id: int, **kwargs) -> Optional[models.Document]:
    db.query(models.Document).filter(
        models.Document.id == document_id
    ).update(kwargs)
    db.commit()
    return db.query(models.Document).filter(
        models.Document.id == document_id
    ).first()

def delete_document(db: Session, document_id: int, user_id: int) -> bool:
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.owner_id == user_id
    ).first()
    if document:
        db.delete(document)
        db.commit()
        return True
    return False

def create_document_analysis(db: Session, document_id: int, 
                           analysis_type: str, result: str, confidence: float) -> models.DocumentAnalysis:
    db_analysis = models.DocumentAnalysis(
        document_id=document_id,
        analysis_type=analysis_type,
        result=result,
        confidence=confidence
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis