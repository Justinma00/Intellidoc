from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from .. import crud, schemas, auth
from ..database import get_db
from ..services.document_processor import DocumentProcessor
from ..services.ai_service import AIService
from ..services.vector_store import VectorStore
import os
import mimetypes
from datetime import datetime

router = APIRouter()
doc_processor = DocumentProcessor()
ai_service = AIService()
vector_store = VectorStore()

@router.post("/upload", response_model=schemas.Document)
async def upload_document(
    file: UploadFile = File(...),
    category: Optional[str] = Form(None),
    current_user: schemas.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file type
    allowed_types = {
        'application/pdf', 'text/plain', 'image/jpeg', 'image/png',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    }
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} not supported"
        )
    
    # Save file
    file_content = await file.read()
    file_path = doc_processor.save_uploaded_file(file_content, file.filename)
    
    # Create document record
    document_create = schemas.DocumentCreate(
        original_filename=file.filename,
        category=category
    )
    
    file_info = {
        "filename": os.path.basename(file_path),
        "file_path": file_path,
        "file_size": len(file_content),
        "mime_type": file.content_type
    }
    
    document = crud.create_document(
        db=db,
        document=document_create,
        user_id=current_user.id,
        file_info=file_info
    )
    
    # Process document asynchronously (simplified - normally would use Celery)
    try:
        # Extract text
        extraction_result = doc_processor.extract_text_from_file(file_path, file.content_type)
        
        if extraction_result.get("text"):
            text = extraction_result["text"]
            
            # Classify document
            classification = ai_service.classify_document(text)
            
            # Generate summary
            summary_result = ai_service.summarize_text(text)
            
            # Generate embeddings
            embeddings = ai_service.get_embeddings([text])
            
            # Update document with processed data
            update_data = {
                "content": text,
                "category": classification.get("category", category),
                "confidence_score": classification.get("confidence", 0.0),
                "summary": summary_result.get("summary", ""),
                "processed_at": datetime.utcnow()
            }
            
            document = crud.update_document(db, document.id, **update_data)
            
            # Add to vector store
            vector_store.add_document(
                doc_id=str(document.id),
                text=text,
                embeddings=embeddings[0] if embeddings else [],
                metadata={
                    "document_id": document.id,
                    "filename": document.original_filename,
                    "category": document.category,
                    "user_id": current_user.id
                }
            )
            
            # Store analysis results
            crud.create_document_analysis(
                db=db,
                document_id=document.id,
                analysis_type="classification",
                result=str(classification),
                confidence=classification.get("confidence", 0.0)
            )
            
    except Exception as e:
        print(f"Error processing document: {e}")
    
    return document

@router.get("/", response_model=List[schemas.Document])
def get_documents(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = Query(None),
    current_user: schemas.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    documents = crud.get_documents(db, user_id=current_user.id, skip=skip, limit=limit)
    
    if category:
        documents = [doc for doc in documents if doc.category == category]
    
    return documents

@router.get("/{document_id}", response_model=schemas.Document)
def get_document(
    document_id: int,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    document = crud.get_document(db, document_id=document_id, user_id=current_user.id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.post("/{document_id}/query")
def query_document(
    document_id: int,
    query: schemas.DocumentQuery,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    document = crud.get_document(db, document_id=document_id, user_id=current_user.id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not document.content:
        raise HTTPException(status_code=400, detail="Document not processed yet")
    
    # Answer question using AI
    result = ai_service.answer_question(query.query, document.content)
    
    return {
        "question": query.query,
        "answer": result.get("answer", ""),
        "confidence": result.get("confidence", 0.0),
        "document_id": document_id,
        "document_title": document.original_filename
    }


@router.post("/search")
def search_documents(
        search_request: schemas.DocumentSearch,  # Accept JSON body
        current_user: schemas.User = Depends(auth.get_current_user),
        db: Session = Depends(get_db)
):
    query = search_request.query
    limit = search_request.limit

    # Generate query embeddings
    query_embeddings = ai_service.get_embeddings([query])

    if not query_embeddings:
        raise HTTPException(status_code=500, detail="Failed to generate query embeddings")

    # Search vector store
    results = vector_store.search_documents(
        query_embeddings=query_embeddings[0],
        n_results=limit,
        where={"user_id": current_user.id}
    )

    return {
        "query": query,
        "results": results,
        "total_found": len(results)
    }
    
    return {
        "query": query,
        "results": results,
        "total_found": len(results)
    }

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    success = crud.delete_document(db, document_id=document_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Remove from vector store
    vector_store.delete_document(str(document_id))
    
    return {"message": "Document deleted successfully"}