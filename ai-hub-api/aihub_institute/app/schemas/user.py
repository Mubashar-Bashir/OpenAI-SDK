from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
import re

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None  # Kept as `str` for flexibility
    profile_picture_url: Optional[str] = None

    class Config:
        orm_mode = True  # Moved here to apply globally

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r"[A-Z]", v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r"\d", v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    user_id: int
    is_active: bool

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password_hash: str