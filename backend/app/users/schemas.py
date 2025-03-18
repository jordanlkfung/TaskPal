from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    password:str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserLoginSchema(UserBase):
    pass

class UserSignUpSchema(UserBase):
    pass
    # confirm_password:str