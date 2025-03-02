from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Candidate(Base):
    __tablename__ = "candidates"
    
    candidate_id = Column(Integer, primary_key=True, index=True)
    photo = Column(String, nullable=True)
    candidate_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    applications = relationship("Application", back_populates="candidate")
