# app/routes/auth.py
from app.database import get_async_db
from app.schemas.auth import RegisterRequest, LoginRequest
from app.crud.user import authenticate_user, get_user_by_email, create_user
from app.jwt import create_access_token, create_refresh_token
from app.config import settings

from fastapi import status,Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

router = APIRouter(prefix='/auth', tags=["auth"])


@router.post("/register")
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_async_db)
):
    existing_user = await get_user_by_email(db, data.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )

    user = await create_user(
        db=db,
        email=data.email,
        password=data.password
    )

    return {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active
    }


@router.post('/login')
async def login_user(
    data: LoginRequest,
    db: AsyncSession = Depends(get_async_db)
):
    user = await authenticate_user(
        db=db,
        email=data.email,
        password=data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)

    return {
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer"
    }

@router.post("/refresh")
async def refresh_token(token:str) :
    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        settings.JWT_ALGORITHM
    )
    
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401,detail="Invalid token type")
    
    email= payload.get("sub")
    
    new_access_token = create_access_token(subject=email)
    
    return{
        "access_token":new_access_token,
        "token_type":"bearer"
    }
    