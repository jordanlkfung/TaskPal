from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    password:str

class User(UserBase):
    id: int


class UserLoginSchema(UserBase):
    pass

class UserSignUpSchema(UserBase):
    pass
    # confirm_password:str
class UserHeaders(BaseModel):
    id:int
    email:str