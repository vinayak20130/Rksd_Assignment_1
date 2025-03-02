from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Opening(Base):
    __tablename__ = "openings"

    opening_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    requirements = Column(String, nullable=False)
    salary_range = Column(String, nullable=False)
    location = Column(String, nullable=False)
    is_remote = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, default=True)
    posted_date = Column(DateTime, server_default=func.now())
    deadline = Column(DateTime, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    experience_required = Column(Integer, nullable=False, default=0)  # ✅ Added this column

    role = relationship("Role", back_populates="openings")
    applications = relationship("Application", back_populates="opening")
