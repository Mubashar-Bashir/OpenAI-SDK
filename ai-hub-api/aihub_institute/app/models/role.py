from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
# from .user import UserRole

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    
    # Relationships
    users: List["UserRole"] = Relationship(back_populates="role")
    