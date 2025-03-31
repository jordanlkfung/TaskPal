from sqlalchemy.ext.asyncio import AsyncSession
from .model import Collection
from .schemas import createCollectionSchema, modifyCollectionSchema
from sqlalchemy import select, delete
from fastapi import HTTPException, status
class CollectionService():
    async def addCollection(self, collection: createCollectionSchema, db:AsyncSession):
        try:
            new_collection = collection.model_dump()
            new_collection_instance = Collection(**new_collection)
            db.add(new_collection_instance)
            #check row changed
            await db.commit()
            db.refresh(new_collection_instance)

            return new_collection_instance.id
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def modifyCollection(self, modified_collection:modifyCollectionSchema, db:AsyncSession):
        try:
            # stmt = select(Collection).where(Collection.id == modified_collection.id)
            collection = await db.get(Collection, modified_collection.id)

            if not collection:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
            
            for attribute, value in modified_collection.model_dump():
                setattr(collection, attribute, value)

            await db.commit(collection)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def deleteCollection(self, collectionId: int, db:AsyncSession):
        try:
            stmt = delete(Collection).where(Collection.id ==collectionId)
            result = await db.execute(stmt)
            #make sure number of rows changed = 1
            if result.rowcount != 1:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except HTTPException as e:
            raise e
        except Exception:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    async def getCollections(self, userId:int, db:AsyncSession):
        try:
            stmt = select(Collection.id, Collection.name).where(Collection.collectionOwner_id == userId)
            result = await db.execute(stmt)
            data = result.fetchall()
            ret = []
            for id, name in data:
                ret.append({
                    "id": id,
                    "name":name,
                })

            return ret
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)