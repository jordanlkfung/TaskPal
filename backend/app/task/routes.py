from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from .service import TaskService
from .schemas import addTaskSchema, updateTaskSchema
from .model import TaskPriority

task_router = APIRouter()
task_service = TaskService()

@task_router.get('/{collection_id}', status_code=status.HTTP_200_OK)
async def getTasks(collection_id:int, db: AsyncSession = Depends(get_db)):
    return await task_service.getTasks(collection_id, db)

@task_router.post('/add', status_code=status.HTTP_201_CREATED)
async def addTask(newTask: addTaskSchema, db: AsyncSession = Depends(get_db)):
    return await task_service.addTask(newTask, db)

@task_router.patch('/', status_code=status.HTTP_204_NO_CONTENT)
async def updateTask(task:updateTaskSchema, db:AsyncSession = Depends(get_db)):
    await task_service.updateTask(task, db)

@task_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTask(id: int, db: AsyncSession = Depends(get_db)):
    await task_service.deleteTask(id, db)

#keep or not keep, patch gives same functionality
#keep for now, allows update of task without sending anything in body
@task_router.patch("/complete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def completeTask(id: int, db:AsyncSession = Depends(get_db)):
    await task_service.completeTask(id, db)
