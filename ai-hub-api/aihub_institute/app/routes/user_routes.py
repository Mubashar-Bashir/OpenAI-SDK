from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.user import User
from typing import List

# Create router for users
user_router = APIRouter()

@user_router.get("/", response_model=List[User], tags=["Users"])
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@user_router.get("/{user_id}", response_model=User, tags=["Users"])
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.user_id == user_id)).first()
    if not user:
        return {"error": "User not found"}
    return user

@user_router.post("/", response_model=User, tags=["Users"])
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@user_router.put("/{user_id}", response_model=User, tags=["Users"])
def update_user(user_id: int, user: User, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.user_id == user_id)).first()
    if not db_user:
        return {"error": "User not found"}
    user.user_id = user_id
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@user_router.delete("/{user_id}", tags=["Users"])
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.user_id == user_id)).first()
    if not user:
        return {"error": "User not found"}
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}