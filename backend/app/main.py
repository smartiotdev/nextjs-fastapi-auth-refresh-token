from app.routes import users, auth

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app=FastAPI(
    title="FastAPI auth backend",
    description="Authentication API using Fast API,async SQLAlchemy and JWT tokens",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers= ["*"]
)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {
        "status":"running","message":"Your Fast API backend is up and running"
    }
    
if __name__ =="__main__":
    print("Fast api backend is starting")
    print("Server is running on http://localhost:8000")
    uvicorn.run("app.main:app",host="0.0.0.0", port=8000,reload=True)
    