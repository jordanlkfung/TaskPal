from fastapi import APIRouter, Depends, status, Response
from .schemas import UserLoginSchema, UserSignUpSchema
from sqlalchemy.ext.asyncio import AsyncSession
from .services import UserService
from app.database import get_db

user_router = APIRouter()
user_service = UserService()

@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: UserLoginSchema, db: AsyncSession = Depends(get_db)):
    """
    Authenticates a user by verifying their email and password.

    This route handles the login request by verifying the user's credentials.
    If successful, a JWT token is generated and returned in the response.

    Args:
        user (UserLoginSchema): The login credentials (email and password) provided by the user.
        db (AsyncSession, optional): The database session dependency, used for querying user data. 
                                      Defaults to the value returned by `get_db`.

    Returns:
        JSONResponse: A response with a JWT token in the Authorization header if login is successful.

    Raises:
        HTTPException: If the email or password is incorrect, a 401 Unauthorized error is raised.
    """
    return await user_service.login(user, db)


@user_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(new_user: UserSignUpSchema, db: AsyncSession = Depends(get_db)):
    """
    Registers a new user by validating the sign-up data and creating the user in the database.

    This route handles the sign-up request. If the email is not already registered,
    the user is created with a hashed password. A JWT token is generated and returned 
    in the response upon successful registration.

    Args:
        new_user (UserSignUpSchema): The user sign-up data (email, password) provided by the user.
        db (AsyncSession, optional): The database session dependency, used for creating the user. 
                                      Defaults to the value returned by `get_db`.

    Returns:
        JSONResponse: A response with a JWT token in the Authorization header and a success message 
                      if the sign-up is successful.

    Raises:
        HTTPException: If the email is already associated with an existing account, 
                       a 409 Conflict error is raised.
    """
    return await user_service.signUp(new_user, db)

