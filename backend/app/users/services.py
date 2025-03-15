from sqlalchemy.orm import Session
from .schemas import UserLoginSchema
import bcrypt

def hash(value:str) -> str:
    return bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode

def compare(value:str, hashed_val:str) -> bool:
    return bcrypt.checkpw(value.encode, hashed_val.encode())

class UserService:
    async def login(self, user: UserLoginSchema, db:Session):
        pass

    async def signUp(self, db:Session):
        pass

    async def logout(self, db:Session):
        pass