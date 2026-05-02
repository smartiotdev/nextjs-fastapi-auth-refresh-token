from pydantic_settings import BaseSettings

class Settings(BaseSettings) :
    DATABASE_URL:str
    SECRET_KEY:str = "secret_key_here"
    
    JWT_SECRET_KEY:str
    JWT_ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MUINUTES:int = 30
    REFRESH_TOKEN_EXPIRE_DAYS:int = 7
    
    class Config:
        env_file = ".env"
        extra = "ignore"
        
        
settings = Settings()