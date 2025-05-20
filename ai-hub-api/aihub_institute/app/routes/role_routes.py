from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.role import Role
from typing import List

# Create router for roles
role_router = APIRouter()

@role_router.get("/", response_model=List[Role], tags=["Roles"])
def get_roles(session: Session = Depends(get_session)):
    return session.exec(select(Role)).all()

@role_router.get("/{role_id}", response_model=Role, tags=["Roles"])
def get_role(role_id: int, session: Session = Depends(get_session)):
    role = session.exec(select(Role).where(Role.id == role_id)).first()
    if not role:
        return {"error": "Role not found"}
    return role

@role_router.post("/", response_model=Role, tags=["Roles"])
def create_role(role: Role, session: Session = Depends(get_session)):
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

@role_router.put("/{role_id}", response_model=Role, tags=["Roles"])
def update_role(role_id: int, role: Role, session: Session = Depends(get_session)):
    db_role = session.exec(select(Role).where(Role.id == role_id)).first()
    if not db_role:
        return {"error": "Role not found"}
    role.id = role_id
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

@role_router.delete("/{role_id}", tags=["Roles"])
def delete_role(role_id: int, session: Session = Depends(get_session)):
    role = session.exec(select(Role).where(Role.id == role_id)).first()
    if not role:
        return {"error": "Role not found"}
    session.delete(role)
    session.commit()
    return {"message": "Role deleted successfully"}