from fastapi import FastAPI
from app.routers.student import router as student_router

app = FastAPI()

app.include_router(student_router)