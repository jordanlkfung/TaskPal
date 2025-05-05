from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from .model import Task
from .schemas import addTaskSchema, updateTaskSchema
from fastapi import HTTPException, status
from app.collection.model import Collection

class TaskService:
    async def getTasks(self, collection_Id:int, db:AsyncSession):
        """
        Retrieve tasks for a specific collection.

        Tasks are ordered by completion status, then by priority, and finally by creation date.

        Args:
            collection_Id (int): The ID of the collection to retrieve tasks from.
            db (AsyncSession): The asynchronous database session.

        Returns:
            List[dict]: A list of task mappings (id, name, priority, creation_date, completed).

        Raises:
            HTTPException: If any error occurs during the query.
        """
        try:
            stmt = select(Task.id, Task.name,Task.priority, Task.creation_date, Task.completed).where(Task.collection_id == collection_Id).order_by(Task.completed)

            stmt = stmt.order_by(Task.priority)
            stmt = stmt.order_by(Task.creation_date)
            result = await db.execute(stmt)

            return result.mappings().all()
        
        except Exception as e:
            print(e)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def addTask(self, data:addTaskSchema, db:AsyncSession):
        """
        Add a new task to the database.

        Args:
            data (addTaskSchema): The schema containing task data.
            db (AsyncSession): The asynchronous database session.

        Returns:
            dict: The created task data with the generated task ID.

        Raises:
            HTTPException: If the task cannot be created or database commit fails.
        """
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
        
    async def deleteTask(self, id:int, db:AsyncSession):
        """
        Delete a task by its ID.

        Args:
            id (int): The ID of the task to delete.
            db (AsyncSession): The asynchronous database session.

        Raises:
            HTTPException: If the task is not found or a database error occurs.
        """
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
        """
        Update an existing task with new values.

        Args:
            updated_task (updateTaskSchema): Schema containing updated task data.
            db (AsyncSession): The asynchronous database session.

        Raises:
            HTTPException: If the task is not found or update fails.
        """
        try:

            stmt = select(Task).where(Task.id == updated_task.id)

            result = await db.execute(stmt)
            task:Task = result.scalar_one_or_none()

            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            for attribute, value in updated_task.model_dump().items():
                setattr(task, attribute, value)
            await db.commit()

        except HTTPException as e:
            raise e
        except Exception as e:
            print(e)
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    async def collectionExists(self, collectionId,db:AsyncSession):
        """
        Check if a collection exists and return its owner's user ID.

        Args:
            collectionId (int): The ID of the collection to check.
            db (AsyncSession): The asynchronous database session.

        Returns:
            int: The user ID of the collection owner.

        Raises:
            HTTPException: If the collection is not found or a database error occurs.
        """
        try:
            stmt = select(Collection.collectionOwner_id).where(Collection.id == collectionId)

            result = await db.execute(stmt)

            data = result.scalar_one_or_none()

            if data:
                return data
            
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def task_belongs_to_user(self, taskId, userId, db:AsyncSession):
        """
        Verify if a task belongs to a given user based on collection ownership.

        Args:
            taskId (int): The ID of the task.
            userId (int): The ID of the user to verify against.
            db (AsyncSession): The asynchronous database session.

        Raises:
            HTTPException: If the task is not found, unauthorized, or a database error occurs.
        """
        try:
            stmt = select(Collection.collectionOwner_id).join(Task).where(Task.id == taskId)

            result = await db.execute(stmt)
            data = result.scalar_one_or_none()

            if not data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
            
            if data == userId:
                return
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))