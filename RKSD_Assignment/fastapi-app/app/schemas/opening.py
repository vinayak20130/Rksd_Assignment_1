from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class OpeningBase(BaseModel):
    title: str
    description: str
    requirements: str
    salary_range: str
    location: str
    is_remote: bool
    is_active: bool = True
    posted_date: datetime = Field(default_factory=datetime.now)
    deadline: datetime
    experience_required: int  # ✅ Add experience required field

class OpeningCreate(OpeningBase):
    pass

class OpeningUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    salary_range: Optional[str] = None
    location: Optional[str] = None
    is_remote: Optional[bool] = None
    is_active: Optional[bool] = None
    deadline: Optional[datetime] = None
    experience_required: Optional[int] = None

class OpeningResponse(OpeningBase):
    opening_id: int  # ✅ Use `opening_id` instead of `id` to match SQLAlchemy model

    class Config:
        from_attributes = True  # ✅ Ensure compatibility with SQLAlchemy models
