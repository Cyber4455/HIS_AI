import json
import uuid
import bcrypt
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from database import get_db
from config import ADMIN_SECRET_KEY
from schemas.auth import RegisterRequest, ChangePasswordRequest, LoginRequest, UserResponse, GuestResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

@router.post("/register", response_model=UserResponse)
async def register(request: RegisterRequest):
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE username = ?", (request.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")
        
        cursor.execute("SELECT id FROM users WHERE email = ?", (request.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already exists")
        
        role = "patient"
        
        password_hash = hash_password(request.password)
        
        cursor.execute(
            """INSERT INTO users (username, email, password_hash, role, status) 
               VALUES (?, ?, ?, ?, ?)""",
            (request.username, request.email, password_hash, role, "active")
        )
        conn.commit()
        
        user_id = cursor.lastrowid
        cursor.execute("SELECT id, username, email, role, created_at FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        
        return UserResponse(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            role=row["role"],
            created_at=row["created_at"]
        )

@router.post("/login", response_model=UserResponse)
async def login(request: LoginRequest):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, password_hash, role, status, created_at FROM users WHERE username = ?", (request.username,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        if not verify_password(request.password, row["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        try:
            user_status = row["status"] if row["status"] else "active"
        except (KeyError, IndexError):
            user_status = "active"
        
        if user_status == "inactive":
            raise HTTPException(status_code=403, detail="Account is inactive. Please contact administrator.")
        
        return UserResponse(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            role=row["role"],
            created_at=row["created_at"]
        )

@router.post("/guest", response_model=GuestResponse)
async def guest_login():
    return GuestResponse(
        session_id=str(uuid.uuid4()),
        role="patient",
        message="Guest session started. Note: Guest sessions are not saved to database."
    )

@router.get("/users", response_model=list[UserResponse])
async def list_users(admin_secret: Optional[str] = Header(None)):
    if admin_secret != ADMIN_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin secret")
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, role, created_at FROM users ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        return [
            UserResponse(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                role=row["role"],
                created_at=row["created_at"]
            )
            for row in rows
        ]

@router.put("/users/{user_id}/role")
async def update_user_role(user_id: int, new_role: str, admin_secret: Optional[str] = Header(None)):
    if admin_secret != ADMIN_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin secret")
    
    if new_role not in ["patient", "doctor"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")
        
        cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
        conn.commit()
        
        return {"message": f"User role updated to {new_role}"}

@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    username: str = None
):
    if not username:
        raise HTTPException(status_code=400, detail="Username required")
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not verify_password(request.current_password, row["password_hash"]):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        
        new_hash = hash_password(request.new_password)
        cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, row["id"]))
        conn.commit()
        
        return {"message": "Password changed successfully"}

@router.put("/users/{user_id}/details")
async def update_user_details(
    user_id: int,
    username: str = None,
    email: str = None,
    admin_secret: Optional[str] = Header(None)
):
    if admin_secret != ADMIN_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin secret")
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")
        
        if username:
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))
        if email:
            cursor.execute("UPDATE users SET email = ? WHERE id = ?", (email, user_id))
        
        conn.commit()
        
        return {"message": "User details updated successfully"}

class ResetPasswordRequest(BaseModel):
    new_password: str

@router.put("/users/{user_id}/reset-password")
async def reset_user_password(
    user_id: int,
    request: ResetPasswordRequest,
    admin_secret: Optional[str] = Header(None)
):
    if admin_secret != ADMIN_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin secret")
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")
        
        new_hash = hash_password(request.new_password)
        cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
        conn.commit()
        
        return {"message": "Password reset successfully"}

@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    status: str,
    admin_secret: Optional[str] = Header(None)
):
    if admin_secret != ADMIN_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin secret")
    
    if status not in ["active", "inactive"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")
        
        cursor.execute("UPDATE users SET status = ? WHERE id = ?", (status, user_id))
        conn.commit()
        
        return {"message": f"User status updated to {status}"}
