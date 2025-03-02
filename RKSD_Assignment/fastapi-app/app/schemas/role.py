from typing import Optional
from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    """Base schema for Role with common attributes"""
    name: str
    description: Optional[str] = None
    is_active: bool = True


class RoleCreate(RoleBase):
    """Schema for creating a new Role"""
    pass


class RoleUpdate(BaseModel):
    """Schema for updating an existing Role, all fields optional"""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class RoleResponse(RoleBase):
    """Schema for role response from API"""
    role_id: int
    
    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
    
    # Map schema field 'name' to model attribute 'role_name'
    name: str = Field(alias="role_name")

