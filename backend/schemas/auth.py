from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: str

class GuestResponse(BaseModel):
    session_id: str
    role: str
    message: str
