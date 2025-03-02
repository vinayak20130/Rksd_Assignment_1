from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.enums import ApplicationStatus  # Import Enum

class ApplicationBase(BaseModel):
    """Base model for Application with common attributes."""
    candidate_id: int = Field(..., description="ID of the candidate applying")
    opening_id: int = Field(..., description="ID of the job opening")
    current_stage: Optional[int] = Field(None, description="Current stage ID of the application")
    status: ApplicationStatus = Field(..., description="Status of the application")  # Using Enum
    application_date: datetime = Field(default_factory=datetime.now, description="Date when candidate applied")

class ApplicationCreate(ApplicationBase):
    """Model for creating a new application."""
    pass

class ApplicationUpdate(BaseModel):
    """Model for updating an existing application."""
    candidate_id: Optional[int] = None
    opening_id: Optional[int] = None
    current_stage: Optional[int] = None
    status: Optional[ApplicationStatus] = None  # Enum used
    application_date: Optional[datetime] = None

class ApplicationResponse(ApplicationBase):
    """Model for returning application data."""
    application_id: int = Field(..., description="Unique identifier for the application")

    class Config:
        from_attributes = True  

class MonthlyApplicationStats(BaseModel):
    """Model for monthly application statistics."""
    year: int = Field(..., description="Year of the applications")
    month: int = Field(..., description="Month of the applications (1-12)")
    count: int = Field(..., description="Count of applications in this month")

    class Config:
        from_attributes = True  

class StageInfo(BaseModel):
    """Model for stage information."""
    current_stage: int = Field(..., description="ID of the stage")
    stage_name: str = Field(..., description="Name of the stage")
    stage_sequence: int = Field(..., description="Sequence number of the stage")

    class Config:
        from_attributes = True

class DetailedApplicationResponse(BaseModel):
    """Model for detailed application response with candidate information."""
    application_id: int = Field(..., description="Unique identifier for the application")
    candidate_name: str = Field(..., description="Name of the candidate")
    rating: Optional[int] = Field(None, description="Rating of the application")
    role_name: str = Field(..., description="Name of the role")
    application_date: datetime = Field(..., description="Date when candidate applied")
    attachments: Optional[str] = Field(None, description="Attachments for the application")
    status: ApplicationStatus = Field(..., description="Status of the application")
    stage: Optional[StageInfo] = Field(None, description="Current stage information")

    class Config:
        from_attributes = True

class ApplicationsByMonthRequest(BaseModel):
    """Model for requesting applications by month."""
    year: Optional[int] = Field(None, description="Year to filter applications (optional, if not provided with month, returns all applications)")
    month: Optional[int] = Field(None, description="Month to filter applications (1-12, optional, if not provided with year, returns all applications)")
    status_filter: Optional[str] = Field("All", description="Filter by status: All, Accepted, Rejected, or Pending")

    @property
    def get_status_enum(self) -> Optional[ApplicationStatus]:
        """Convert status filter string to enum value."""
        if self.status_filter == "Accepted":
            return ApplicationStatus.ACCEPTED
        elif self.status_filter == "Rejected":
            return ApplicationStatus.REJECTED
        elif self.status_filter == "Pending":
            return ApplicationStatus.PENDING
        return None  # "All" or invalid values return None

class ExperienceDetail(BaseModel):
    """Model for experience details."""
    experience_id: int
    company_name: str
    position: str
    start_date: datetime
    end_date: Optional[datetime] = None
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

class RoleStage(BaseModel):
    """Model for stage information for a role."""
    stage_id: int
    stage_name: str
    stage_sequence: int
    
    class Config:
        from_attributes = True

class ApplicationDetailResponse(BaseModel):
    """Model for detailed application response with experiences and all stages."""
    application_id: int
    candidate_id: int
    candidate_name: str
    role_id: int
    role_name: str
    current_stage_id: int
    current_stage_name: str
    current_stage_sequence: int
    status: ApplicationStatus
    application_date: datetime
    experiences: List[ExperienceDetail]
    role_stages: List[RoleStage]
    
    class Config:
        from_attributes = True

class StageUpdateRequest(BaseModel):
    """Model for updating application stage."""
    action: str = Field(..., description="Action to take: 'next' to advance to next stage, 'reject' to reject the application")
