"""
Admin Route — System-level analytics and summaries.
"""
from fastapi import APIRouter
from database import get_admin_summary

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/summary")
async def get_summary():
    """Get system-level analytics for admin view."""
    data = get_admin_summary()
    return data
