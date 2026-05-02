from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/users",tags=["users"])

@router.get('/me')
async def get_me(current_user= Depends(get_current_user)):
    return{
        "id":current_user.id,
        "email":current_user.email,
        "is_active":current_user.is_active,
    }