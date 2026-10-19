from fastapi import FastAPI
from app.database import Base, engine
from app.models.student import Student
from app.routers.student import router as student_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(student_router)