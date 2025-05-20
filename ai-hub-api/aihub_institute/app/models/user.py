from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import date
from .student import Student

class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    email: str = Field(index=True, unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None  # Updated to `date` type
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    profile_picture_url: Optional[str] = None
    is_active: bool = Field(default=True)  # Removed Optional wrapper

    # Relationships
    # student_profile: Optional["Student"] = Relationship(back_populates="user")
    student: Optional["Student"] = Relationship(back_populates="user")
    roles: List["UserRole"] = Relationship(back_populates="user")