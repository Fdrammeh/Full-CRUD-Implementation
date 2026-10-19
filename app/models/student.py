from sqlalchemy import Boolean, Column, DateTime, Integer, String, Float, func
from app.database import Base


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String,unique=True, nullable=False, index=True)
    major = Column(String, nullable=True)
    gpa = Column(Float, nullable=True)
    grade_level = Column(Integer, nullable=True)  # New field for grade level
    is_enrolled = Column(Boolean, default =True, nullable=False)  # New field for enrollment status 
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    


