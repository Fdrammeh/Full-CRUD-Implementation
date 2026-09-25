from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StudentCreate(BaseModel):
    name: str
    email: str
    major: Optional[str] = None        
    gpa:Optional[float] = Field(default=None, ge=0.0, le=4.0)

class StudentUpdate(BaseModel):
    name: str
    email: str
    major: Optional[str]
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)   

class StudentPatch(BaseModel): 
    name: Optional[str] = None 
    email: Optional[str] = None 
    major: Optional[str] = None 
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)

class StudentResponse(BaseModel): 
    id: int 
    name: str 
    email: str 
    major: Optional[str] = None 
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)

    class Config: 
        from_attributes = True       
 