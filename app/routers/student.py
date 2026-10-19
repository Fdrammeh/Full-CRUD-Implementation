from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student
from app.schemas.student import (StudentCreate, StudentUpdate, StudentPatch, StudentResponse)
from typing import Optional
from fastapi import Response, status

router = APIRouter(prefix="/students", tags=["Students"])

def get_student_or_404(student_id: int, db: Session) -> Student:
    """Return a student or raise a 404 error."""
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

#POST /students - creating a student
@router.post("/", response_model=StudentResponse, status_code=201) 
def create_student(student: StudentCreate, db: Session = Depends(get_db)):

    existing_student = ( 
        db.query(Student) .filter(Student.email == student.email) .first() )

    if existing_student:
        raise HTTPException(
            status_code=409,
            detail="A student with this email alreayd exixts"

        )

    new_student = Student( 
        name=student.name, 
        email=student.email, 
        major=student.major, 
        gpa=student.gpa, 
        grade_level = student.grade_level,
        is_enrolled = student.is_enrolled,
    )


    db.add(new_student) 
    db.commit() 
    db.refresh(new_student) 
    return new_student

# 2. GET /students - Get all students 
# Optional filters: major and min_gpa 
@router.get("/", response_model=list[StudentResponse]) 
def get_students( 
    major: Optional[str] = Query(default=None), min_gpa: Optional[float] = Query(
        default=None, 
        ge=0.0, 
        le=4.0),
    db: Session = Depends(get_db) 

):
    query = db.query(Student)

    if major is not None: 
        query = query.filter(Student.major == major) 
    if min_gpa is not None: query = query.filter(Student.gpa >= min_gpa) 
    return query.all()

# 3. GET /students/{id} - Get one student
@router.get("/{student_id}", response_model=StudentResponse) 

def get_student(student_id: int, db: Session = Depends(get_db)): 
    student = get_student_or_404(student_id, db)
    return student

# 4. PUT /students/{id} - Full replacement
@router.put("/{student_id}", response_model=StudentResponse) 
def update_student( 
    student_id: int, 
    student_data:StudentUpdate, 
    db: Session = Depends(get_db), ): 

    student = get_student_or_404(student_id, db)

# Check whether the new email belongs to another student
    existing_student = ( 
        db.query(Student) 
        .filter( 
            Student.email == student_data.email, Student.id != student_id, ) .first() )

    if existing_student:
        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists.")
        

    student.name = student_data.name 
    student.email = student_data.email 
    student.major = student_data.major 
    student.gpa = student_data.gpa 
    db.commit() 
    db.refresh(student) 
    return student


#PATCH /students/{id} - Partial update 

@router.patch("/{student_id}", response_model=StudentResponse)
def patch_student(
    student_id: int,
    student_data: StudentPatch,
    db: Session = Depends(get_db),
):
    # Find the student or return a 404 error
    student = get_student_or_404(student_id, db)

    # Get only the fields the client provided
    updates = student_data.model_dump(exclude_unset=True)

    # Check for duplicate email if email is being changed
    if "email" in updates:
        existing_student = (
            db.query(Student)
            .filter(
                Student.email == updates["email"],
                Student.id != student_id,
            )
            .first()
        )

        if existing_student:
            raise HTTPException(
                status_code=409,
                detail="A student with this email already exists.",
            )

    # Apply every provided update, not just email updates
    for field, value in updates.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)

    return student


# 6. DELETE /students/{id} - Delete a student
@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    # Find the student or raise a 404 error
    student = get_student_or_404(student_id, db)

    # Delete the student
    db.delete(student)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
