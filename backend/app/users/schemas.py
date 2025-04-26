from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    password:str

class User(UserBase):
    id: int


class UserLoginSchema(UserBase):
    pass

class UserSignUpSchema(UserBase):
    pass

class UserHeaders(BaseModel):
    id:int
    email:str