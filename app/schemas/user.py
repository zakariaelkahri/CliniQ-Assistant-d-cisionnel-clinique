from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str
    
class UserResponse(UserBase):
    id: int 
    role: str
    
    class Config:
        from_attributes = True
        
        