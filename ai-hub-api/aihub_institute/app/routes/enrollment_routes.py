from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.enrollment import Enrollment
from typing import List

# Create router for enrollments
enrollment_router = APIRouter()

@enrollment_router.get("/", response_model=List[Enrollment], tags=["Enrollments"])
def get_enrollments(session: Session = Depends(get_session)):
    return session.exec(select(Enrollment)).all()

@enrollment_router.get("/{enrollment_id}", response_model=Enrollment, tags=["Enrollments"])
def get_enrollment(enrollment_id: int, session: Session = Depends(get_session)):
    enrollment = session.exec(select(Enrollment).where(Enrollment.id == enrollment_id)).first()
    if not enrollment:
        return {"error": "Enrollment not found"}
    return enrollment

@enrollment_router.post("/", response_model=Enrollment, tags=["Enrollments"])
def create_enrollment(enrollment: Enrollment, session: Session = Depends(get_session)):
    session.add(enrollment)
    session.commit()
    session.refresh(enrollment)
    return enrollment

@enrollment_router.put("/{enrollment_id}", response_model=Enrollment, tags=["Enrollments"])
def update_enrollment(enrollment_id: int, enrollment: Enrollment, session: Session = Depends(get_session)):
    db_enrollment = session.exec(select(Enrollment).where(Enrollment.id == enrollment_id)).first()
    if not db_enrollment:
        return {"error": "Enrollment not found"}
    enrollment.id = enrollment_id
    session.add(enrollment)
    session.commit()
    session.refresh(enrollment)
    return enrollment

@enrollment_router.delete("/{enrollment_id}", tags=["Enrollments"])
def delete_enrollment(enrollment_id: int, session: Session = Depends(get_session)):
    enrollment = session.exec(select(Enrollment).where(Enrollment.id == enrollment_id)).first()
    if not enrollment:
        return {"error": "Enrollment not found"}
    session.delete(enrollment)
    session.commit()
    return {"message": "Enrollment deleted successfully"}