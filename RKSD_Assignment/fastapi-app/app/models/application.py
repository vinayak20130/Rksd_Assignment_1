from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, func
from sqlalchemy.orm import relationship
from app.database.connection import Base
from app.models.enums import ApplicationStatus

class Application(Base):
    __tablename__ = "applications"

    application_id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id"), nullable=False)
    opening_id = Column(Integer, ForeignKey("openings.opening_id"), nullable=False)
    rating = Column(Integer, nullable=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    application_date = Column(DateTime, nullable=False, default=func.now())
    attachments = Column(String, nullable=True)
    status = Column(Enum(ApplicationStatus), nullable=False, default=ApplicationStatus.PENDING)
    current_stage = Column(Integer, ForeignKey("stages.stage_id"), nullable=False, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    role = relationship("Role", back_populates="applications")
    experiences = relationship("Experience", back_populates="application", cascade="all, delete-orphan")
    candidate = relationship("Candidate", back_populates="applications")
    opening = relationship("Opening", back_populates="applications")
    stage = relationship("Stage", back_populates="applications", foreign_keys=[current_stage])
