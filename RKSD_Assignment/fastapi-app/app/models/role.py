from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Role(Base):
    __tablename__ = "roles"
    
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    stages = relationship("Stage", back_populates="role")
    applications = relationship("Application", back_populates="role")
    openings = relationship("Opening", back_populates="role")

