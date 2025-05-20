from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from .enrollment import Enrollment

class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    code: str = Field(index=True, unique=True)
    credit_hours: int
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    enrollment: List["Enrollment"] = Relationship(back_populates="course")