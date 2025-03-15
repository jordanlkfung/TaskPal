from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from .model import Task
from .schemas import addTaskSchema
class TaskService:
    async def getTasks(self, collection_Id:int, db:Session):
        stmt = select(Task).where(Task.collection_id == collection_Id)
        return db.execute(stmt)

    async def addTask(self, data:addTaskSchema, db:Session):
        pass

    async def completeTask(self):
        pass

    async def deleteTask(self):
        pass

    async def updateTask(self):
        pass
