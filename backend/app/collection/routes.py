from fastapi import APIRouter, Depends, status
from .service import CollectionService
from .schemas import createCollectionSchema, modifyCollectionSchema
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

collection_router = APIRouter()
collection_service = CollectionService()

@collection_router.get('/get/{userId}')
async def getUserCollections(userId:int, db:AsyncSession = Depends(get_db)):
    return await collection_service.getCollections(userId, db)

@collection_router.post("/add", status_code=status.HTTP_201_CREATED)
async def addCollection(new_collection:createCollectionSchema, db:AsyncSession =Depends(get_db)):
    print(new_collection)
    res = await collection_service.addCollection(new_collection, db)
    return res

@collection_router.delete("/{collection_id}")
async def deleteCollection(collection_id:int):
    collection_service.deleteCollection(collection_id)

@collection_router.patch("/{collection_id}")
async def modifyCollection(collection:modifyCollectionSchema):
    collection_service.modifyCollection(collection)