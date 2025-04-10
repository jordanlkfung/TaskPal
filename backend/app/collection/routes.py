from fastapi import APIRouter, Depends, status
from .service import CollectionService
from .schemas import createCollectionSchema, modifyCollectionSchema
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.authentication import get_user_from_token

collection_router = APIRouter()
collection_service = CollectionService()

# @collection_router.get('/get/{userId}')
@collection_router.get('/get')
async def getUserCollections(userId:int = Depends(get_user_from_token), db:AsyncSession = Depends(get_db)):
    return await collection_service.getCollections(userId, db)

@collection_router.post("/add", status_code=status.HTTP_201_CREATED)
async def addCollection(new_collection:createCollectionSchema, db:AsyncSession =Depends(get_db)):
    res = await collection_service.addCollection(new_collection, db)
    return {"collection_id":res}

@collection_router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteCollection(collection_id:int, userId:int = Depends(get_user_from_token), db:AsyncSession = Depends(get_db)):
    await collection_service.collection_exists(collection_id, db)
    await collection_service.authenticate_collection_owner(userId, collection_id, db)
    await collection_service.deleteCollection(collection_id, db)

@collection_router.patch("/")
async def modifyCollection(collection:modifyCollectionSchema, userId:int = Depends(get_user_from_token),  db:AsyncSession = Depends(get_db)):
   await collection_service.collection_exists(collection.id, db)
   await collection_service.authenticate_collection_owner(userId, collection.id, db)
   await collection_service.modifyCollection(collection, db)