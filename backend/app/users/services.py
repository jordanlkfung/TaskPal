from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserLoginSchema, UserSignUpSchema
import bcrypt
from sqlalchemy import select
from .model import User
from fastapi import HTTPException, status

# Hash password function
def hash(value: str) -> str:
    return bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()  # Decoding to return a string

# Compare password function
def compare(value: str, hashed_val: str) -> bool:
    return bcrypt.checkpw(value.encode(), hashed_val.encode())

class UserService:
    
    # Login function
    async def login(self, user: UserLoginSchema, db: AsyncSession):
        stmt = select(User.id, User.password).where(User.email == user.email)
        result = await db.execute(stmt)
        data = result.fetchone() 
        
        if data:
            # Checking if the provided password matches the stored hashed password
            if compare(user.password, data.password):
                return data.id  # Return the user id from the result data, not from the result object
        
        # If no user is found or the passwords don't match, raise HTTP exception
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Invalid email or password")

    # Sign-up function
    async def signUp(self, user: UserSignUpSchema, db: AsyncSession):
        '''Sign Up service, raises HTTP exception if user already exists, otherwise creates user'''
        
        # Check if user email already exists
        stmt = select(User).where(User.email == user.email)
        result = await db.execute(stmt)
        user_exists = result.fetchone()
        
        if user_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account already exists")
        
        # Hash the password and create user
        user_dict = user.model_dump()
        user_dict['password'] = hash(user_dict['password']) 
        
        # Create a new user instance
        user_instance = User(**user_dict)
        
        # Add to the session and commit the changes to the database
        db.add(user_instance)
        await db.commit()
        await db.refresh(user_instance)  # Refresh to ensure all fields are populated

        return user_instance.id  # Return the user id after creation


    # Logout function (Currently does nothing)
    async def logout(self, db: Session):
        pass 
