from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ExperienceBase(BaseModel):
    """Base schema for Experience with shared attributes"""
    application_id: int  # Link experience to an application
    company_name: str
    position: str
    start_date: datetime
    end_date: Optional[datetime] = None
    description: Optional[str] = None


class ExperienceCreate(ExperienceBase):
    """Schema for creating a new experience"""
    pass


class ExperienceResponse(ExperienceBase):
    """Schema for returning experience data"""
    experience_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Ensures SQLAlchemy ORM compatibility


class ExperienceUpdate(BaseModel):
    """Schema for updating an existing experience"""
    application_id: Optional[int] = None
    company_name: Optional[str] = None
    position: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None
