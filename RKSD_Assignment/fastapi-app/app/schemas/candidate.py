from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class CandidateBase(BaseModel):
    """Base Pydantic model for candidate data validation"""
    photo: Optional[str] = None
    candidate_name: str
    email: EmailStr
    phone_number: str


class CandidateCreate(CandidateBase):
    """Pydantic model for validating candidate creation data"""
    pass


class CandidateUpdate(BaseModel):
    """Pydantic model for validating candidate update data with optional fields"""
    photo: Optional[str] = None
    candidate_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None


class CandidateResponse(CandidateBase):
    """Pydantic model for candidate response data including database fields"""
    candidate_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

