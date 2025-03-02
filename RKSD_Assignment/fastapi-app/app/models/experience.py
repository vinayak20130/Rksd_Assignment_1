from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Experience(Base):
    __tablename__ = "experiences"
    
    experience_id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.application_id"), nullable=False)
    company_name = Column(String, nullable=False)  # Renamed from 'company'
    position = Column(String, nullable=False)  # New field
    description = Column(String, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    application = relationship("Application", back_populates="experiences")
