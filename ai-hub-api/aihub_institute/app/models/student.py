from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
# from .user import User
# from enrollment import Enrollment

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id", unique=True)
    registration_number: str = Field(index=True, unique=True)
    date_of_birth: Optional[datetime] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())
    
    # Relationships
    user: "User" = Relationship(back_populates="student")
    enrollment: List["Enrollment"] = Relationship(back_populates="student")