from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.course import Course
from typing import List

# Create router for courses
course_router = APIRouter()

@course_router.get("/", response_model=List[Course], tags=["Courses"])
def get_courses(session: Session = Depends(get_session)):
    return session.exec(select(Course)).all()

@course_router.get("/{course_id}", response_model=Course, tags=["Courses"])
def get_course(course_id: int, session: Session = Depends(get_session)):
    course = session.exec(select(Course).where(Course.id == course_id)).first()
    if not course:
        return {"error": "Course not found"}
    return course

#post endpoint to create course
@course_router.post("/", response_model=Course, tags=["Courses"])
def create_course(course: Course, session: Session = Depends(get_session)):
    session.add(course)
    session.commit()
    session.refresh(course)
    return course
#put endpoint to update course
@course_router.put("/{course_id}", response_model=Course, tags=["Courses"])
def update_course(course_id: int, course: Course, session: Session = Depends(get_session)):
    db_course = session.exec(select(Course).where(Course.id == course_id)).first()
    if not db_course:
        return {"error": "Course not found"}
    course.id = course_id
    session.add(course)
    session.commit()
    session.refresh(course)
    return course
#delete endpoint to delete course
@course_router.delete("/{course_id}", tags=["Courses"])
def delete_course(course_id: int, session: Session = Depends(get_session)):
    course = session.exec(select(Course).where(Course.id == course_id)).first()
    if not course:
        return {"error": "Course not found"}
    session.delete(course)
    session.commit()
    return {"message": "Course deleted successfully"}
# This code defines a FastAPI router for managing courses in an educational application. It includes endpoints to get all courses, get a specific course by ID, create a new course, update an existing course, and delete a course. The router uses SQLModel for database interactions and FastAPI's dependency injection system to manage database sessions.
# The endpoints are tagged with "Courses" for better organization in the API documentation.
# The code also includes error handling for cases where a course is not found in the database.
# The response models are defined using Pydantic, which allows for type-safe and well-structured
# responses.
# The code is designed to be modular and reusable, making it easy to integrate into a larger FastAPI application.
# The use of SQLModel and FastAPI's dependency injection system makes the code efficient and easy to
# maintain.