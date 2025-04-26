from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from .service import TaskService
from .schemas import addTaskSchema, updateTaskSchema
from .model import TaskPriority
from app.utils.authentication import get_user_from_token

task_router = APIRouter()
task_service = TaskService()


    
@task_router.get('/{collection_id}', status_code=status.HTTP_200_OK)
async def getTasks(collection_id:int, db: AsyncSession = Depends(get_db), userId = Depends(get_user_from_token)):
    user = await task_service.collectionExists(collection_id,db)
    if user != userId:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return await task_service.getTasks(collection_id, db)

@task_router.post('/add', status_code=status.HTTP_201_CREATED)
async def addTask(newTask: addTaskSchema, db: AsyncSession = Depends(get_db), userId = Depends(get_user_from_token)):
    user = await task_service.collectionExists(newTask.collection_id,db)
    if user != userId:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return await task_service.addTask(newTask, db)

@task_router.patch('/', status_code=status.HTTP_204_NO_CONTENT)
async def updateTask(task:updateTaskSchema, db:AsyncSession = Depends(get_db), userId = Depends(get_user_from_token)):
    await task_service.task_belongs_to_user(task.id, userId, db)
    await task_service.updateTask(task, db)

@task_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTask(id: int, db: AsyncSession = Depends(get_db), userId = Depends(get_user_from_token)):
    await task_service.task_belongs_to_user(id, userId, db)
    await task_service.deleteTask(id, db)

