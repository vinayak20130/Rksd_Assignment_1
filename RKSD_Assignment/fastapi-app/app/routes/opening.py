from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.opening import Opening
from app.database.connection import get_db
from app.schemas.opening import OpeningCreate, OpeningResponse, OpeningUpdate

router = APIRouter(
    tags=["openings"],
    responses={404: {"description": "Opening not found"}}
)


@router.get("/", response_model=List[OpeningResponse], status_code=status.HTTP_200_OK)
async def get_all_openings(
    skip: int = 0, 
    limit: int = 100, 
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve all job openings with optional filtering by location.
    """
    query = db.query(Opening)
    
    if location:
        query = query.filter(Opening.location == location)
        
    openings = query.offset(skip).limit(limit).all()
    
    return [OpeningResponse.model_validate(opening) for opening in openings]


@router.get("/{opening_id}", response_model=OpeningResponse, status_code=status.HTTP_200_OK)
async def get_opening_by_id(opening_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific job opening by ID.
    """
    opening = db.query(Opening).filter(Opening.opening_id == opening_id).first()
    if not opening:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opening with ID {opening_id} not found"
        )
    
    return OpeningResponse.model_validate(opening)


@router.post("/", response_model=OpeningResponse, status_code=status.HTTP_201_CREATED)
async def create_opening(opening_data: OpeningCreate, db: Session = Depends(get_db)):
    """
    Create a new job opening.
    """
    db_opening = Opening(**opening_data.model_dump())  # Convert Pydantic to SQLAlchemy
    db.add(db_opening)
    db.commit()
    db.refresh(db_opening)
    
    return OpeningResponse.model_validate(db_opening)


@router.put("/{opening_id}", response_model=OpeningResponse, status_code=status.HTTP_200_OK)
async def update_opening(opening_id: int, opening_data: OpeningUpdate, db: Session = Depends(get_db)):
    """
    Update an existing job opening.
    """
    db_opening = db.query(Opening).filter(Opening.opening_id == opening_id).first()
    if not db_opening:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opening with ID {opening_id} not found"
        )

    for key, value in opening_data.model_dump(exclude_unset=True).items():  # Only update provided fields
        setattr(db_opening, key, value)

    db.commit()
    db.refresh(db_opening)

    return OpeningResponse.model_validate(db_opening)


@router.delete("/{opening_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_opening(opening_id: int, db: Session = Depends(get_db)):
    """
    Delete a job opening.
    """
    db_opening = db.query(Opening).filter(Opening.opening_id == opening_id).first()
    if not db_opening:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opening with ID {opening_id} not found"
        )
        
    db.delete(db_opening)
    db.commit()
    return None
