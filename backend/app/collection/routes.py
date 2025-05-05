from fastapi import APIRouter, Depends, status
from .service import CollectionService
from .schemas import collectionBase, modifyCollectionSchema
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.authentication import get_user_from_token

collection_router = APIRouter()
collection_service = CollectionService()

@collection_router.get('/get')
async def getUserCollections(userId:int = Depends(get_user_from_token), db:AsyncSession = Depends(get_db)):
    """
    Retrieves all collections for the currently authenticated user.

    Parameters:
        userId (int): The ID of the authenticated user (injected via dependency).
        db (AsyncSession): The database session (injected via dependency).

    Returns:
        List[Dict]: A list of the user's collections along with task counts.
    """
    return await collection_service.getCollections(userId, db)

@collection_router.post("/add", status_code=status.HTTP_201_CREATED)
async def addCollection(new_collection:collectionBase, userId:int = Depends(get_user_from_token), db:AsyncSession =Depends(get_db)):
    """
    Creates a new collection for the authenticated user.

    Parameters:
        new_collection (collectionBase): The collection data to be added.
        userId (int): The ID of the authenticated user (injected via dependency).
        db (AsyncSession): The database session (injected via dependency).

    Returns:
        dict: The ID of the newly created collection.
    """
    res = await collection_service.addCollection(new_collection,userId, db)
    return {"collection_id":res}

@collection_router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteCollection(collection_id:int, userId:int = Depends(get_user_from_token), db:AsyncSession = Depends(get_db)):
    """
    Deletes a collection by ID if the authenticated user is the owner.

    Parameters:
        collection_id (int): The ID of the collection to delete.
        userId (int): The ID of the authenticated user (injected via dependency).
        db (AsyncSession): The database session (injected via dependency).

    Returns:
        None: Returns 204 No Content on successful deletion.

    Raises:
        HTTPException: 
            - 404 if the collection does not exist.
            - 401 if the user is not authorized.
            - 500 if an internal error occurs.
    """
    await collection_service.collection_exists(collection_id, db)
    await collection_service.authenticate_collection_owner(userId, collection_id, db)
    await collection_service.deleteCollection(collection_id, db)

@collection_router.patch("/")
async def modifyCollection(collection:modifyCollectionSchema, userId:int = Depends(get_user_from_token),  db:AsyncSession = Depends(get_db)):
    """
    Modifies an existing collection if the authenticated user is the owner.

    Parameters:
        collection (modifyCollectionSchema): The updated collection data.
        userId (int): The ID of the authenticated user (injected via dependency).
        db (AsyncSession): The database session (injected via dependency).

    Returns:
        None: Returns 200 OK on successful update.

    Raises:
        HTTPException:
            - 404 if the collection does not exist.
            - 401 if the user is not authorized.
            - 500 if an internal error occurs.
    """
    await collection_service.collection_exists(collection.id, db)
    await collection_service.authenticate_collection_owner(userId, collection.id, db)
    await collection_service.modifyCollection(collection, db)
