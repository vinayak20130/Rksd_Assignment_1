from pydantic import BaseModel
from typing import Optional

class StageBase(BaseModel):
    """Base class for Stage schema with common attributes."""
    stage_name: str
    stage_sequence: int
    is_active: bool = True

class StageCreate(StageBase):
    """Schema for creating a new Stage."""
    role_id: int

class StageUpdate(BaseModel):
    """Schema for updating an existing Stage."""
    stage_name: Optional[str] = None
    stage_sequence: Optional[int] = None
    is_active: Optional[bool] = None

class StageResponse(StageBase):
    """Schema for Stage response data."""
    stage_id: int
    role_id: int

    class Config:
        from_attributes = True  # ✅ Fix for Pydantic v2
