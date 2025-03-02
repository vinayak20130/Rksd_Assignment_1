from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate

router = APIRouter(
    tags=["Roles"],
    responses={404: {"description": "Role not found"}}
)


@router.get("/", response_model=List[RoleResponse])
async def get_all_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all roles with pagination support.
    """
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role_by_id(role_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific role by its ID.
    """
    role = db.query(Role).filter(Role.role_id == role_id).first()
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    """
    Create a new role.
    """
    db_role = Role(
        role_name=role.name,
        description=role.description,
        is_active=role.is_active if hasattr(role, 'is_active') else True
    )
    
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    
    return db_role


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    """
    Update an existing role.
    """
    db_role = db.query(Role).filter(Role.role_id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    
    # Update the role attributes with field mapping
    update_data = role.dict(exclude_unset=True)
    if 'name' in update_data:
        db_role.role_name = update_data['name']
    if 'description' in update_data:
        db_role.description = update_data['description']
    if 'is_active' in update_data:
        db_role.is_active = update_data['is_active']
    
    db.commit()
    db.refresh(db_role)
    
    return db_role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: int, db: Session = Depends(get_db)):
    """
    Delete a role.
    """
    db_role = db.query(Role).filter(Role.role_id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    
    db.delete(db_role)
    db.commit()
    
    return None

