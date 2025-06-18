from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    original_filename: str
    category: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    filename: str
    file_size: int
    mime_type: str
    content: Optional[str] = None
    summary: Optional[str] = None
    confidence_score: Optional[float] = None
    language: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class DocumentQuery(BaseModel):
    query: str
    document_ids: Optional[List[int]] = None

class DocumentAnalysisResult(BaseModel):
    analysis_type: str
    result: str
    confidence: float

class DocumentSearch(BaseModel):
    query: str
    limit: Optional[int] = 10