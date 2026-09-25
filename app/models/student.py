from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String,unique=True, nullable=False, index=True)
    major = Column(String, nullable=True)
    gpa = Column(Float, nullable=True)

