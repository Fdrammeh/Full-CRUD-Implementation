from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class StudentCreate(BaseModel):
    name: str
    email: str
    major: Optional[str] = None        
    gpa:Optional[float] = Field(default=None, ge=0.0, le=4.0)
    grade_level: Optional[int] = Field(default=None, ge=1, le=12)
    is_enrolled: bool = True

class StudentUpdate(BaseModel):
    name: str
    email: str
    major: Optional[str]
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)   
    grade_level: Optional[int] = Field(default=None, ge=1, le=12)
    is_enrolled: bool = True

class StudentPatch(BaseModel): 
    name: Optional[str] = None 
    email: Optional[str] = None 
    major: Optional[str] = None 
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)
    grade_level: Optional[int] = Field(default=None, ge=1, le=12)
    is_enrolled: Optional[bool] = None

class StudentResponse(BaseModel): 
    id: int 
    name: str 
    email: str   
    major: Optional[str] = None 
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)
    grade_level: Optional[int] = Field(default=None, ge=1, le=12)
    is_enrolled: Optional[bool] = Field(default=True, nullable=False)
    created_at: datetime

       

    model_config = ConfigDict(from_attributes=True) 
 