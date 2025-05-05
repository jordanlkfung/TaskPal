from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from .service import TaskService
from .schemas import addTaskSchema, updateTaskSchema
from app.utils.authentication import get_user_from_token

task_router = APIRouter()
task_service = TaskService()


    
@task_router.get('/{collection_id}', status_code=status.HTTP_200_OK)
async def getTasks(collection_id:int, db: AsyncSession = Depends(get_db), userId = Depends(get_user_from_token)):
    """
    Retrieve all tasks from a given collection.

    Ensures that the requesting user owns the collection before fetching tasks.

    Args:
        collection_id (int): The ID of the task collection.
        db (AsyncSession): The database session (injected by FastAPI).
        userId (int): The ID of the authenticated user. Parsed from JWT token

    Returns:
        List[dict]: A list of tasks belonging to the specified collection.

    Raises:
        HTTPException: If the user is unauthorized or the collection does not exist.
    """
    user = await task_service.collectionExists(collection_id,db)
    if user != userId:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return await task_service.getTasks(collection_id, db)

@task_router.post('/add', status_code=status.HTTP_201_CREATED)
async def addTask(newTask: addTaskSchema, db: AsyncSession = Depends(get_db), userId = Depends(get_user_from_token)):
    """
    Add a new task to a collection.

    Verifies that the user owns the collection before allowing the task to be added.

    Args:
        newTask (addTaskSchema): Schema containing task data to be added.
        db (AsyncSession): The database session (injected by FastAPI).
        userId (int): The ID of the authenticated user. Parsed from JWT token

    Returns:
        dict: The newly created task with its generated ID.

    Raises:
        HTTPException: If the user is unauthorized or the collection does not exist.
    """
    user = await task_service.collectionExists(newTask.collection_id,db)
    if user != userId:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return await task_service.addTask(newTask, db)

@task_router.patch('/', status_code=status.HTTP_204_NO_CONTENT)
async def updateTask(task:updateTaskSchema, db:AsyncSession = Depends(get_db), userId = Depends(get_user_from_token)):
    """
    Update an existing task.

    Checks that the task belongs to the authenticated user before applying updates.

    Args:
        task (updateTaskSchema): Schema with updated task information.
        db (AsyncSession): The database session (injected by FastAPI).
        userId (int): The ID of the authenticated user. Parsed from JWT token

    Raises:
        HTTPException: If the task does not belong to the user or update fails.
    """
    await task_service.task_belongs_to_user(task.id, userId, db)
    await task_service.updateTask(task, db)

@task_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTask(id: int, db: AsyncSession = Depends(get_db), userId = Depends(get_user_from_token)):
    """
    Delete a task by its ID.

    Ensures the task belongs to the requesting user before deletion.

    Args:
        id (int): The ID of the task to delete.
        db (AsyncSession): The database session (injected by FastAPI).
        userId (int): The ID of the authenticated user. Parsed from JWT token

    Raises:
        HTTPException: If the task does not belong to the user or deletion fails.
    """
    await task_service.task_belongs_to_user(id, userId, db)
    await task_service.deleteTask(id, db)

