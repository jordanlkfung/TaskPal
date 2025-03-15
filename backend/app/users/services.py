from sqlalchemy.orm import Session
from schemas import UserLoginSchmea
class UserService:
    async def login(self, user: UserLoginSchmea, db:Session):
        pass

    async def signUp(self):
        pass

    async def logout(self, db:Session):
        pass