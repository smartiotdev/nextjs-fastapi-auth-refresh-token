#app/crud/user.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User
from app.security import verify_password, hash_password

async def create_user(
    db:AsyncSession,
    email:str,
    password:str,
) ->User:
    hashed_pw= hash_password(password)
    
    user = User(
        email= email,
        hashed_password = hashed_pw
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user

async def get_user_by_email(
    db:AsyncSession,
    email:str
) ->User|None:
    
    result = await db.execute(
        select(User).where(User.email ==email)
    )
    
    return result.scalar_one_or_none()

async def authenticate_user(
    db:AsyncSession,
    email:str,
    password:str
) ->User|None:
    user = await get_user_by_email(db,email)
    if not User :
        return None
    if not verify_password(password,user.hashed_password):
        return None
    
    
    if not user.is_active:
        return None
    
    
    return user