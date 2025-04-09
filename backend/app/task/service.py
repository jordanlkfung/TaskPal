from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, desc
from .model import Task, TaskPriority
from .schemas import addTaskSchema, updateTaskSchema
from fastapi import HTTPException, status
from datetime import datetime


class TaskService:
    async def getTasks(self, collection_Id:int, db:AsyncSession, order:str):
        try:
            stmt = select(Task.id, Task.name,Task.priority, Task.creation_date, Task.completed).where(Task.collection_id == collection_Id).order_by(Task.completed)

            if order == 'priority':
                stmt = stmt.order_by(Task.priority)
                
            stmt = stmt.order_by(Task.creation_date)
            result = await db.execute(stmt)

            data = result.fetchall()

            res = []
            for id, name, priority, create_date, completed in data:
                res.append({"id":id,
                            "name":name,
                            "priority":priority,
                            "create_date":create_date,
                            "completed":completed})
            return res
        except Exception as e:
            print(e)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def addTask(self, data:addTaskSchema, db:AsyncSession):
        try:
            new_task_dict = data.model_dump()
            new_task_instance = Task(**new_task_dict)
            db.add(new_task_instance)
            await db.commit()

            await db.refresh(new_task_instance) #this can get the task_id
            new_task_dict['id'] = new_task_instance.id
            
            return new_task_dict
        
        except Exception as e:
            print(e)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def completeTask(self, id:int, db:AsyncSession):
        try:
            stmt = select(Task).where(Task.id == id)

            result = await db.execute(stmt)
            task = result.scalar_one_or_none()

            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            task.completed = True
            task.completed_date = datetime.now()
        
            await db.commit()
        
            return id
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def deleteTask(self, id:int, db:AsyncSession):
        try:
            stmt = delete(Task).where(Task.id == id)

            result = await db.execute(stmt)

            if result.rowcount != 1:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            await db.commit()

        except HTTPException as e:
            raise e
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


        

    async def updateTask(self, updated_task:updateTaskSchema, db:AsyncSession):
        try:

            stmt = select(Task).where(Task.id == updated_task.id)

            result = await db.execute(stmt)
            task:Task = result.scalar_one_or_none()

            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            for attribute, value in updated_task.model_dump().items():
                print(attribute)
                setattr(task, attribute, value)
            await db.commit()

        except HTTPException as e:
            raise e
        except Exception as e:
            print(e)
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    