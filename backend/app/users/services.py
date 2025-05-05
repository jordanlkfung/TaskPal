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
    """
    Hashes a plain-text password using bcrypt.

    Args:
        value (str): The plain-text password to hash.

    Returns:
        str: The hashed password as a UTF-8 string.
    """
    return bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()


# Compare password function
def compare(value: str, hashed_val: str) -> bool:
    """
    Compares a plain-text password with its hashed version.

    Args:
        value (str): The plain-text password.
        hashed_val (str): The hashed password for comparison.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return bcrypt.checkpw(value.encode(), hashed_val.encode())


def setHeaders(user_info: UserHeaders, success_message: str) -> JSONResponse:
    """
    Sets HTTP response headers with a JWT auth token and a success message.

    Args:
        user_info (UserHeaders): The user information to encode in the token.
        success_message (str): The message to include in the response content.

    Returns:
        JSONResponse: A response object with Authorization header and message.
    """
    auth_token = jwt_service.create_token(user_info.model_dump(mode='python'))
    res = JSONResponse(headers={"Authorization": "Bearer " + auth_token}, content={"message": success_message})
    return res


class UserService:

    async def login(self, user: UserLoginSchema, db: AsyncSession):
        """
        Authenticates a user by verifying email and password.

        Args:
            user (UserLoginSchema): Login credentials provided by the user.
            db (AsyncSession): The database session for querying user data.

        Returns:
            JSONResponse: A response with an auth token if login is successful.

        Raises:
            HTTPException: If email or password is incorrect.
        """
        stmt = select(User.id, User.password).where(User.email == user.email)
        result = await db.execute(stmt)
        data: User = result.one_or_none() 
        
        if data:
            if compare(user.password, data.password):
                res = setHeaders(UserHeaders(email=user.email, id=data.id), success_message="Login Successful")
                res.status_code = status.HTTP_200_OK
                return res
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Invalid email or password")


    async def signUp(self, user: UserSignUpSchema, db: AsyncSession):
        """
        Registers a new user. If the email already exists, raises an error.

        Args:
            user (UserSignUpSchema): The user registration data.
            db (AsyncSession): The database session for creating the user.

        Returns:
            JSONResponse: A response with an auth token if sign-up is successful.

        Raises:
            HTTPException: If an account with the given email already exists.
        """
        stmt = select(User).where(User.email == user.email)
        result = await db.execute(stmt)
        user_exists = result.fetchone()
        
        if user_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
        
        user_dict = user.model_dump()
        user_dict['password'] = hash(user_dict['password']) 
        
        user_instance = User(**user_dict)
        
        db.add(user_instance)
        await db.commit()
        await db.refresh(user_instance) #allows us to return userId

        res = setHeaders(UserHeaders(id=user_instance.id, email=user_instance.email), success_message="Sign up successful")
        res.status_code = status.HTTP_201_CREATED
        return res
