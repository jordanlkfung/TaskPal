from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from .service import TaskService
from .schemas import addTaskSchema, updateTaskSchema

task_router = APIRouter()
task_service = TaskService()

@task_router.get('/{collection_id}')
async def getTasks(collection_id:int, db: Session = Depends(get_db)):
    await task_service.getTasks(collection_id, db)

@task_router.post('/{collection_id}/add')
async def addTask(newTask: addTaskSchema, db: Session = Depends(get_db)):
    pass

@task_router.patch('/{id}')
async def updateTask(task:updateTaskSchema):
    pass

@task_router.delete("/{id}")
async def deleteTask(id: int, db: Session = Depends(get_db)):
    pass

#keep or not keep, patch gives same functionality
@task_router.patch("/complete/{id}")
async def completeTask(id: int, db:Session = Depends(get_db)):
    pass