from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func, extract
from datetime import datetime

from app.database.connection import get_db
from app.models.application import Application
from app.models.candidate import Candidate
from app.models.role import Role
from app.models.stage import Stage
from app.models.experience import Experience
from app.models.enums import ApplicationStatus
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationResponse, MonthlyApplicationStats, DetailedApplicationResponse, ApplicationsByMonthRequest, StageInfo, ApplicationDetailResponse, ExperienceDetail, RoleStage, StageUpdateRequest
from app.utils.pdf_generator import generate_application_pdf

router = APIRouter(
    responses={404: {"description": "Application not found"}}
)

@router.get("/", response_model=List[ApplicationResponse])
async def get_applications(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Retrieve all applications with pagination.
    """
    applications = db.query(Application).offset(skip).limit(limit).all()

    return [ApplicationResponse.model_validate(app) for app in applications]



@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int, 
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific application by ID.
    """
    application = db.query(Application).filter(Application.application_id == application_id).first()
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Application with ID {application_id} not found"
        )
    return application


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    application: ApplicationCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new application.
    """
    db_application = Application(**application.dict())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: int, 
    application: ApplicationUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing application.
    """
    db_application = db.query(Application).filter(Application.application_id == application_id).first()
    if db_application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Application with ID {application_id} not found"
        )
        
    update_data = application.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_application, key, value)
    
    db.commit()
    db.refresh(db_application)
    return db_application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    application_id: int, 
    db: Session = Depends(get_db)
):
    """
    Delete an application.
    """
    db_application = db.query(Application).filter(Application.application_id == application_id).first()
    if db_application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Application with ID {application_id} not found"
        )
        
    db.delete(db_application)
    db.commit()
    return None

@router.post("/by-month/detailed", response_model=List[DetailedApplicationResponse])
async def get_detailed_applications_by_month(
    request: ApplicationsByMonthRequest,
    db: Session = Depends(get_db)
):
    """
    Retrieve detailed applications for a specific month and year.

    Returns detailed application data including candidate name, rating, role, stage, 
    application date, and attachments. Can be filtered by status (All, Accepted, Rejected, Pending).
    
    If year or month are not provided, returns all applications regardless of date.
    """
    # Initialize the query
    query = (
        db.query(
            Application.application_id,
            Candidate.candidate_name,
            Role.role_name,
            Application.rating,
            Application.application_date,
            Application.attachments,
            Application.status,
            Stage.stage_id,   # ✅ Fetch full stage details
            Stage.stage_name,
            Stage.stage_sequence
        )
        .join(Candidate, Application.candidate_id == Candidate.candidate_id)
        .join(Role, Application.role_id == Role.role_id)
        .outerjoin(Stage, Stage.stage_id == Application.current_stage)  # ✅ Ensure this join is correct
    )

    # Apply date filters only if both year and month are provided
    if request.year is not None and request.month is not None:
        query = query.filter(
            extract('year', Application.application_date) == request.year,
            extract('month', Application.application_date) == request.month
        )

    # Apply status filter if not "All"
    if request.get_status_enum is not None:
        query = query.filter(Application.status == request.get_status_enum)

    results = query.all()

    # Transform results into response model
    detailed_applications = [
        DetailedApplicationResponse(
            application_id=row[0],
            candidate_name=row[1],
            role_name=row[2],
            rating=row[3],
            application_date=row[4],
            attachments=row[5],
            status=row[6],
            stage=StageInfo(  # ✅ Fix: Create full StageInfo object
                current_stage=row[7],  # stage_id
                stage_name=row[8],  # stage_name
                stage_sequence=row[9]  # stage_sequence
            ) if row[7] else None  # If stage_id is None, set stage=None
        )
        for row in results
    ]

    return detailed_applications

@router.get("/{application_id}/details", response_model=ApplicationDetailResponse)
async def get_application_details(
    application_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve detailed information about an application including:
    - Candidate information
    - Current application status and stage
    - All experiences of the candidate for this application
    - All stages for the role associated with this application
    """
    # Get the application with related data
    application = (
        db.query(
            Application.application_id,
            Application.candidate_id,
            Candidate.candidate_name,
            Application.role_id,
            Role.role_name,
            Application.current_stage,
            Stage.stage_name,
            Stage.stage_sequence,
            Application.status,
            Application.application_date
        )
        .join(Candidate, Application.candidate_id == Candidate.candidate_id)
        .join(Role, Application.role_id == Role.role_id)
        .join(Stage, Application.current_stage == Stage.stage_id)
        .filter(Application.application_id == application_id)
        .first()
    )
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found"
        )
    
    # Get all experiences for this application
    experiences = (
        db.query(Experience)
        .filter(Experience.application_id == application_id)
        .all()
    )
    
    # Get all stages for the role associated with this application
    role_stages = (
        db.query(Stage)
        .filter(Stage.role_id == application[3])  # application[3] is role_id
        .order_by(Stage.stage_sequence)
        .all()
    )
    
    # Construct the response
    return ApplicationDetailResponse(
        application_id=application[0],
        candidate_id=application[1],
        candidate_name=application[2],
        role_id=application[3],
        role_name=application[4],
        current_stage_id=application[5],
        current_stage_name=application[6],
        current_stage_sequence=application[7],
        status=application[8],
        application_date=application[9],
        experiences=[
            ExperienceDetail(
                experience_id=exp.experience_id,
                company_name=exp.company_name,
                position=exp.position,
                start_date=exp.start_date,
                end_date=exp.end_date,
                description=exp.description
            ) for exp in experiences
        ],
        role_stages=[
            RoleStage(
                stage_id=stage.stage_id,
                stage_name=stage.stage_name,
                stage_sequence=stage.stage_sequence
            ) for stage in role_stages
        ]
    )

@router.post("/{application_id}/update-stage", response_model=ApplicationResponse)
async def update_application_stage(
    application_id: int,
    request: StageUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Update an application's stage and status.
    
    - If action is 'next': Advances the application to the next stage if available.
      If it's the last stage, changes status to ACCEPTED.
    - If action is 'reject': Changes the application status to REJECTED.
    """
    # Get the application
    application = db.query(Application).filter(Application.application_id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found"
        )
    
    # Handle rejection
    if request.action.lower() == "reject":
        application.status = ApplicationStatus.REJECTED
        db.commit()
        db.refresh(application)
        return application
    
    # Handle advancing to next stage
    if request.action.lower() == "next":
        # Get all stages for this role
        role_stages = (
            db.query(Stage)
            .filter(Stage.role_id == application.role_id)
            .order_by(Stage.stage_sequence)
            .all()
        )
        
        if not role_stages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No stages found for this role"
            )
        
        # Find current stage and determine if it's the last one
        current_stage = None
        next_stage = None
        
        for i, stage in enumerate(role_stages):
            if stage.stage_id == application.current_stage:
                current_stage = stage
                if i < len(role_stages) - 1:
                    next_stage = role_stages[i + 1]
                break
        
        if not current_stage:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current stage not found in role stages"
            )
        
        # If there's a next stage, advance to it
        if next_stage:
            application.current_stage = next_stage.stage_id
        else:
            # If it's the last stage, mark as accepted
            application.status = ApplicationStatus.ACCEPTED
        
        db.commit()
        db.refresh(application)
        return application
    
    # If action is neither 'next' nor 'reject'
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid action. Must be 'next' or 'reject'"
    )

@router.get("/{application_id}/pdf", response_class=Response)
async def generate_application_pdf_endpoint(
    application_id: int,
    db: Session = Depends(get_db)
):
    """
    Generate a PDF document with detailed information about an application.
    
    The PDF includes:
    - Candidate information
    - Role and application details
    - Current stage and status
    - Work experience history
    - All stages for the role with their status (completed, current, pending)
    """
    # Reuse the logic from get_application_details to fetch the data
    application = (
        db.query(
            Application.application_id,
            Application.candidate_id,
            Candidate.candidate_name,
            Application.role_id,
            Role.role_name,
            Application.current_stage,
            Stage.stage_name,
            Stage.stage_sequence,
            Application.status,
            Application.application_date,
            Application.rating
        )
        .join(Candidate, Application.candidate_id == Candidate.candidate_id)
        .join(Role, Application.role_id == Role.role_id)
        .join(Stage, Application.current_stage == Stage.stage_id)
        .filter(Application.application_id == application_id)
        .first()
    )
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found"
        )
    
    # Get all experiences for this application
    experiences = (
        db.query(Experience)
        .filter(Experience.application_id == application_id)
        .all()
    )
    
    # Get all stages for the role associated with this application
    role_stages = (
        db.query(Stage)
        .filter(Stage.role_id == application[3])  # application[3] is role_id
        .order_by(Stage.stage_sequence)
        .all()
    )
    
    # Prepare data for PDF generation
    application_data = {
        "application_id": application[0],
        "candidate_id": application[1],
        "candidate_name": application[2],
        "role_id": application[3],
        "role_name": application[4],
        "current_stage_id": application[5],
        "current_stage_name": application[6],
        "current_stage_sequence": application[7],
        "status": application[8],
        "application_date": application[9],
        "rating": application[10],
        "experiences": experiences,
        "role_stages": role_stages
    }
    
    # Generate the PDF
    pdf_buffer = generate_application_pdf(application_data)
    
    # Return the PDF as a downloadable file
    filename = f"application_{application_id}_{application[2].replace(' ', '_')}.pdf"
    
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
