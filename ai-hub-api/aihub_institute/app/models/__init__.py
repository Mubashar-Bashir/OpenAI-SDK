from .user import User
from .role import Role
from .student import Student
from .course import Course
from .enrollment import Enrollment
from .user_role import UserRole

# For SQLModel to discover all tables
__all__ = ["User", "UserRole", "Role", "Student", "Course", "Enrollment"]