from sqlalchemy.ext.asyncio import AsyncSession
from .model import Collection
from ..task.model import Task
from .schemas import collectionBase, modifyCollectionSchema
from sqlalchemy import select, delete, func
from fastapi import HTTPException, status
class CollectionService():
    async def addCollection(self, collection: collectionBase, userId, db:AsyncSession):
        """
        Asynchronously adds a new collection to the database for the specified user.

        Parameters:
            collection (collectionBase): The collection data to be added.
            userId (Any): The ID of the user who owns the collection.
            db (AsyncSession): The asynchronous database session.

        Returns:
            int: The ID of the newly created collection.

        Raises:
            HTTPException: If an error occurs while adding the collection to the database.
        """
        try:
            new_collection_instance = Collection(name=collection.name, collectionOwner_id=userId)
            db.add(new_collection_instance)
            #check row changed
            await db.commit()
            db.refresh(new_collection_instance)

            return new_collection_instance.id
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def modifyCollection(self, modified_collection: modifyCollectionSchema, db: AsyncSession):
        """
        Asynchronously modifies an existing collection in the database.

        Parameters:
            modified_collection (modifyCollectionSchema): The updated data for the collection.
            db (AsyncSession): The asynchronous database session.

        Raises:
            HTTPException: 
                - 404 if the collection is not found.
                - 500 if an internal server error occurs.
        """
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

    async def deleteCollection(self, collectionId: int, db: AsyncSession):
        """
        Asynchronously deletes a collection from the database by its ID.

        Parameters:
            collectionId (int): The ID of the collection to delete.
            db (AsyncSession): The asynchronous database session.

        Raises:
            HTTPException: 
                - 404 if the collection is not found.
                - 500 if an internal server error occurs.
        """

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
        
    async def getCollections(self, userId: int, db: AsyncSession):
        """
        Asynchronously retrieves all collections for a given user, including task count per collection.

        Parameters:
            userId (int): The ID of the user whose collections are to be retrieved.
            db (AsyncSession): The asynchronous database session.

        Returns:
            List[Dict]: A list of dictionaries containing collection IDs, names, and task counts.

        Raises:
            HTTPException: 500 if an internal server error occurs.
        """

        try:
            stmt = select(Collection.id, Collection.name, func.count(Task.name).label("Number of Tasks")).join(Task, isouter=True).where(
                Collection.collectionOwner_id == userId).group_by(Collection.id)
            print(stmt)
            result = await db.execute(stmt)

            return result.mappings().all()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    
    async def authenticate_collection_owner(self, userId: int, collection_id: int, db: AsyncSession):
        """
        Authenticates whether the given user is the owner of the specified collection.

        Parameters:
            userId (int): The ID of the user to authenticate.
            collection_id (int): The ID of the collection to check ownership for.
            db (AsyncSession): The asynchronous database session.

        Raises:
            HTTPException: 
                - 401 if the user is not authorized (not the owner).
                - 500 if an internal server error occurs.
        """

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
    
    async def collection_exists(self, collection_id: int, db: AsyncSession):
        """
        Checks whether a collection exists in the database by its ID.

        Parameters:
            collection_id (int): The ID of the collection to check.
            db (AsyncSession): The asynchronous database session.

        Raises:
            HTTPException: 
                - 404 if the collection is not found.
                - 500 if an internal server error occurs.
        """

        stmt = select(Collection.id).where(Collection.id==collection_id)
        try:
            result = await db.execute(stmt)

            data = result.one_or_none()
            
            if not data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    