from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.models.experience import Experience
from app.schemas.experience import ExperienceCreate, ExperienceResponse, ExperienceUpdate

router = APIRouter(
    tags=["experiences"],
    responses={404: {"description": "Experience not found"}}
)


@router.get("/", response_model=List[ExperienceResponse])
async def get_experiences(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Retrieve all experiences with pagination.
    """
    experiences = db.query(Experience).offset(skip).limit(limit).all()
    return experiences


@router.get("/{experience_id}", response_model=ExperienceResponse)
async def get_experience_by_id(
    experience_id: int, 
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific experience by its ID.
    """
    experience = db.query(Experience).filter(Experience.experience_id == experience_id).first()
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Experience with ID {experience_id} not found"
        )
    return experience


@router.post("/", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED)
async def create_experience(
    experience: ExperienceCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new experience record.
    """
    db_experience = Experience(**experience.dict())
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience


@router.put("/{experience_id}", response_model=ExperienceResponse)
async def update_experience(
    experience_id: int, 
    experience: ExperienceUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing experience record.
    """
    db_experience = db.query(Experience).filter(Experience.experience_id == experience_id).first()
    if not db_experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Experience with ID {experience_id} not found"
        )
    
    # Update the experience with the provided data
    update_data = experience.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_experience, key, value)
        
    db.commit()
    db.refresh(db_experience)
    return db_experience


@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(
    experience_id: int, 
    db: Session = Depends(get_db)
):
    """
    Delete an experience record.
    """
    db_experience = db.query(Experience).filter(Experience.experience_id == experience_id).first()
    if not db_experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Experience with ID {experience_id} not found"
        )
    
    db.delete(db_experience)
    db.commit()
    return None

