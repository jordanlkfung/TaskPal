from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    password:str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserLoginSchmea(UserBase):
    pass

class UserSignUpSchema(UserBase):
    pass
    confirm_password:str
# class BookUpdateSchema(BaseModel):
#     title:str
#     author:str
#     publisher:str
#     page_count:int
#     language:str


# class Book(BaseModel):
#     id: int
#     title: str
#     author: str
#     publisher: str
#     published_date: str
#     page_count: int
#     language: str