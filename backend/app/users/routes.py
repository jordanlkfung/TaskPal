from fastapi import APIRouter, Depends, status
from .schemas import UserLoginSchema
from sqlalchemy.orm import Session
from .services import UserService
from app.database import get_db

user_router = APIRouter()
user_service = UserService()

@user_router.get("/login", status_code=status.HTTP_200_OK)
async def login(user:UserLoginSchema, db: Session = Depends(get_db)):
    res = await user_service.login(user, db)
    return {"message":"hello"}

@user_router.get('/signup', status_code=status.HTTP_201_CREATED)
async def signup():
    return "std"