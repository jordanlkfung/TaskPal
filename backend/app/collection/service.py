from sqlalchemy.ext.asyncio import AsyncSession
from .model import Collection
from ..task.model import Task
from .schemas import collectionBase, modifyCollectionSchema
from sqlalchemy import select, delete, func
from fastapi import HTTPException, status
class CollectionService():
    async def addCollection(self, collection: collectionBase, userId, db:AsyncSession):
        try:
            new_collection = collection.model_dump()
            new_collection_instance = Collection(name=collection.name, collectionOwner_id=userId)
            db.add(new_collection_instance)
            #check row changed
            await db.commit()
            db.refresh(new_collection_instance)

            return new_collection_instance.id
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def modifyCollection(self, modified_collection:modifyCollectionSchema, db:AsyncSession):
        try:
            collection = await db.get(Collection, modified_collection.id)
            if not collection:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
            
            for attribute, value in modified_collection.model_dump().items():
                setattr(collection, attribute, value)

            await db.commit()
        except HTTPException as e:
            raise e
        except Exception as e:
            print(e)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def deleteCollection(self, collectionId: int, db:AsyncSession):
        try:
            stmt = delete(Collection).where(Collection.id ==collectionId)
            result = await db.execute(stmt)
            #make sure number of rows changed = 1
            if result.rowcount != 1:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            await db.commit()
        except HTTPException as e:
            raise e
        except Exception:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    async def getCollections(self, userId:int, db:AsyncSession):
        try:
            stmt = select(Collection.id, Collection.name, func.count(Task.name).label("Number of Tasks")).join(Task, isouter=True).where(
                Collection.collectionOwner_id == userId).group_by(Collection.id)
            print(stmt)
            result = await db.execute(stmt)

            return result.mappings().all()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    
    async def authenticate_collection_owner(self, userId:int, collection_id:int, db:AsyncSession):
        stmt = select(Collection.collectionOwner_id).where(
            (Collection.id == collection_id) & (Collection.collectionOwner_id == userId)
            )
        
        try:
            result = await db.execute(stmt)

            data = result.one_or_none()
            if not data:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    async def collection_exists(self, collection_id:int, db:AsyncSession):
        stmt = select(Collection.id).where(Collection.id==collection_id)
        try:
            result = await db.execute(stmt)

            data = result.one_or_none()
            
            if not data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
