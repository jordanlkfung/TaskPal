from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserLoginSchema, UserSignUpSchema, UserHeaders
import bcrypt
from sqlalchemy import select
from .model import User
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from ..utils.authentication import jwt_service

# Hash password function
def hash(value: str) -> str:
    return bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()

# Compare password function
def compare(value: str, hashed_val: str) -> bool:
    return bcrypt.checkpw(value.encode(), hashed_val.encode())

def setHeaders(user_info:UserHeaders, success_message:str) -> JSONResponse:
    # auth_token = jwt_service.create_token({"id": user_info.id, "email":user_info.email})
    auth_token = jwt_service.create_token(user_info.model_dump(mode='python'))
    res = JSONResponse(headers={"Authorization":"Bearer " + auth_token}, content={"message":success_message})
    return res
class UserService:
    
    # Login function
    async def login(self, user: UserLoginSchema, db: AsyncSession):
        stmt = select(User.id, User.password).where(User.email == user.email)
        result = await db.execute(stmt)
        data:User = result.one_or_none() 
        
        if data:
            # Checking if the provided password matches the stored hashed password
            if compare(user.password, data.password):
                res = setHeaders(UserHeaders(email=user.email, id=data.id), success_message="Login Successful")
                res.status_code = status.HTTP_200_OK
                return res

        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Invalid email or password")



    # Sign-up function
    async def signUp(self, user: UserSignUpSchema, db: AsyncSession):
        '''Sign Up service, raises HTTP exception if user already exists, otherwise creates user'''
        print(user)
        # Check if user email already exists
        stmt = select(User).where(User.email == user.email)
        result = await db.execute(stmt)
        user_exists = result.fetchone()
        
        if user_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account already exists")
        
        # Hash the password and create user
        user_dict = user.model_dump()
        print(user_dict)
        user_dict['password'] = hash(user_dict['password']) 
        
        # Create a new user instance
        user_instance = User(**user_dict)
        
        # Add to the session and commit the changes to the database
        db.add(user_instance)
        await db.commit()
        await db.refresh(user_instance)  #adds id to user_instance

        res = setHeaders(UserHeaders(id=user_instance.id, email=user_instance.email), success_message="Sign up successful")
        res.status_code = status.HTTP_201_CREATED
        return res

    async def logout(self, db: Session):
        pass 
