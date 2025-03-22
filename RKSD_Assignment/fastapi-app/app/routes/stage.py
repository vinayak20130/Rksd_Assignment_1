from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.models.stage import Stage
from app.schemas.stage import StageCreate, StageResponse, StageUpdate

router = APIRouter(
    responses={404: {"description": "Stage not found"}}
)

@router.get("/", response_model=List[StageResponse])
async def get_all_stages(db: Session = Depends(get_db)):
    """Retrieve all stages and convert to Pydantic models"""
    stages = db.query(Stage).all()
    return [StageResponse.model_validate(stage) for stage in stages]  # ✅ Ensures proper data conversion

@router.get("/{stage_id}", response_model=StageResponse)
async def get_stage_by_id(stage_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific stage by ID"""
    stage = db.query(Stage).filter(Stage.stage_id == stage_id).first()
    if stage is None:
        raise HTTPException(status_code=404, detail="Stage not found")
    
    return StageResponse.model_validate(stage)  # ✅ Fixes response validation error

@router.post("/", response_model=StageResponse, status_code=status.HTTP_201_CREATED)
async def create_stage(stage: StageCreate, db: Session = Depends(get_db)):
    """Create a new stage"""
    db_stage = Stage(**stage.model_dump())  # ✅ Correct use of model_dump() for Pydantic v2
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    
    return StageResponse.model_validate(db_stage)  # ✅ Fixes response validation error

@router.put("/{stage_id}", response_model=StageResponse)
async def update_stage(stage_id: int, stage: StageUpdate, db: Session = Depends(get_db)):
    """Update an existing stage"""
    db_stage = db.query(Stage).filter(Stage.stage_id == stage_id).first()
    if db_stage is None:
        raise HTTPException(status_code=404, detail="Stage not found")
    
    for key, value in stage.model_dump(exclude_unset=True).items():  # ✅ Corrected data handling
        setattr(db_stage, key, value)

    db.commit()
    db.refresh(db_stage)

    return StageResponse.model_validate(db_stage)  # ✅ Fixes response validation error

@router.delete("/{stage_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stage(stage_id: int, db: Session = Depends(get_db)):
    """Delete a stage"""
    db_stage = db.query(Stage).filter(Stage.stage_id == stage_id).first()
    if db_stage is None:
        raise HTTPException(status_code=404, detail="Stage not found")
    
    db.delete(db_stage)
    db.commit()
    return None
