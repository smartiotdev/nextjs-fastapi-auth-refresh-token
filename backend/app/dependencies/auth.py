#app/dependencies/auth.py
from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_async_db
from app.crud.user import get_user_by_email


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

async def get_current_user(
  token:str = Depends(oauth2_scheme),
  db:AsyncSession = Depends(get_async_db)  
):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        email:str |None = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401,detail="Invalid token")
        user = await get_user_by_email(db,email)
        
        if not user or not user.is_active :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
        
        return user
        
    except:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )