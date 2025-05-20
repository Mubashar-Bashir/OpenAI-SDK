from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.user_role import UserRole
from typing import List

# Create router for user roles
user_role_router = APIRouter()

@user_role_router.get("/", response_model=List[UserRole], tags=["UserRoles"])
def get_user_roles(session: Session = Depends(get_session)):
    return session.exec(select(UserRole)).all()

@user_role_router.get("/{user_role_id}", response_model=UserRole, tags=["UserRoles"])
def get_user_role(user_role_id: int, session: Session = Depends(get_session)):
    user_role = session.exec(select(UserRole).where(UserRole.id == user_role_id)).first()
    if not user_role:
        return {"error": "UserRole not found"}
    return user_role

@user_role_router.post("/", response_model=UserRole, tags=["UserRoles"])
def create_user_role(user_role: UserRole, session: Session = Depends(get_session)):
    session.add(user_role)
    session.commit()
    session.refresh(user_role)
    return user_role

@user_role_router.put("/{user_role_id}", response_model=UserRole, tags=["UserRoles"])
def update_user_role(user_role_id: int, user_role: UserRole, session: Session = Depends(get_session)):
    db_user_role = session.exec(select(UserRole).where(UserRole.id == user_role_id)).first()
    if not db_user_role:
        return {"error": "UserRole not found"}
    user_role.id = user_role_id
    session.add(user_role)
    session.commit()
    session.refresh(user_role)
    return user_role

@user_role_router.delete("/{user_role_id}", tags=["UserRoles"])
def delete_user_role(user_role_id: int, session: Session = Depends(get_session)):
    user_role = session.exec(select(UserRole).where(UserRole.id == user_role_id)).first()
    if not user_role:
        return {"error": "UserRole not found"}
    session.delete(user_role)
    session.commit()
    return {"message": "UserRole deleted successfully"}