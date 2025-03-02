from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate, CandidateResponse, CandidateUpdate

router = APIRouter(
    tags=["candidates"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[CandidateResponse])
async def get_candidates(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Retrieve all candidates with pagination.
    """
    candidates = db.query(Candidate).offset(skip).limit(limit).all()
    return candidates

@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: int, 
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific candidate by ID.
    """
    candidate = db.query(Candidate).filter(Candidate.candidate_id == candidate_id).first()
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CandidateResponse)
async def create_candidate(
    candidate_data: CandidateCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new candidate.
    """
    candidate = Candidate(**candidate_data.model_dump())
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

@router.put("/{candidate_id}", status_code=status.HTTP_200_OK)
async def update_candidate(
    candidate_id: int,
    candidate_data: CandidateUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing candidate.
    """
    db_candidate = db.query(Candidate).filter(Candidate.candidate_id == candidate_id).first()
    
    if not db_candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with ID {candidate_id} not found"
        )

    update_data = candidate_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_candidate, key, value)

    db.commit()
    db.refresh(db_candidate)

    return {
        "photo": db_candidate.photo,
        "candidate_name": db_candidate.candidate_name,
        "email": db_candidate.email,
        "phone_number": db_candidate.phone_number
    }

@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a candidate.
    """
    candidate = db.query(Candidate).filter(Candidate.candidate_id == candidate_id).first()
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    db.delete(candidate)
    db.commit()
    return None

