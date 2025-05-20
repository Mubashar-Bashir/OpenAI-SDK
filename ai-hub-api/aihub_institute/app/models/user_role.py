from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class UserRole(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    role_id: int = Field(foreign_key="role.id")

    # Relationships
    user: "User" = Relationship(back_populates="roles")
    role: "Role" = Relationship(back_populates="users")