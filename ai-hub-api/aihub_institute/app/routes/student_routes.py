from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.student import Student
from typing import List

# Create router for students
student_router = APIRouter()

@student_router.get("/", response_model=List[Student], tags=["Students"])
def get_students(session: Session = Depends(get_session)):
    return session.exec(select(Student)).all()

@student_router.get("/{student_id}", response_model=Student, tags=["Students"])
def get_student(student_id: int, session: Session = Depends(get_session)):
    student = session.exec(select(Student).where(Student.id == student_id)).first()
    if not student:
        return {"error": "Student not found"}
    return student

@student_router.post("/", response_model=Student, tags=["Students"])
def create_student(student: Student, session: Session = Depends(get_session)):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@student_router.put("/{student_id}", response_model=Student, tags=["Students"])
def update_student(student_id: int, student: Student, session: Session = Depends(get_session)):
    db_student = session.exec(select(Student).where(Student.id == student_id)).first()
    if not db_student:
        return {"error": "Student not found"}
    student.id = student_id
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@student_router.delete("/{student_id}", tags=["Students"])
def delete_student(student_id: int, session: Session = Depends(get_session)):
    student = session.exec(select(Student).where(Student.id == student_id)).first()
    if not student:
        return {"error": "Student not found"}
    session.delete(student)
    session.commit()
    return {"message": "Student deleted successfully"}