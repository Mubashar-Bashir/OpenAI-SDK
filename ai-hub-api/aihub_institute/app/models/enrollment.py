from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
# from .student import Student
# from .course import Course

class Enrollment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    course_id: int = Field(foreign_key="course.id")
    enrollment_date: datetime = Field(default_factory=datetime.utcnow)
    grade: Optional[float] = None
    status: str = "active"  # active, completed, dropped
    
    # Relationships
    student: "Student" = Relationship(back_populates="enrollment")
    course: "Course" = Relationship(back_populates="enrollment")
    
    class Config:
        table_name = "enrollment"