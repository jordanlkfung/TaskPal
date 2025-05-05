from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """
    Base user schema containing common fields used for authentication.

    Attributes:
        email (EmailStr): The user's email address, validated as a proper email.
        password (str): The user's plain-text password.
    """
    email: EmailStr
    password: str


class User(UserBase):
    """
    Full user schema including user ID, typically used for internal representation.

    Inherits:
        UserBase: Includes email and password fields.

    Attributes:
        id (int): Unique identifier of the user.
    """
    id: int


class UserLoginSchema(UserBase):
    """
    Schema for user login, inheriting from UserBase.

    Used to validate login requests.
    """
    pass


class UserSignUpSchema(UserBase):
    """
    Schema for user registration (sign-up), inheriting from UserBase.

    Used to validate user registration input.
    """
    pass


class UserHeaders(BaseModel):
    """
    Schema for user information stored in headers or tokens.

    Attributes:
        id (int): Unique identifier of the user.
        email (str): Email address of the user.
    """
    id: int
    email: str
