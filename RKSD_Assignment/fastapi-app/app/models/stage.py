from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Stage(Base):
    __tablename__ = "stages"
    
    stage_id = Column(Integer, primary_key=True, index=True)
    stage_name = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    stage_sequence = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    role = relationship("Role", back_populates="stages")
    applications = relationship("Application", back_populates="stage")
