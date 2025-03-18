from sqlalchemy.ext.asyncio import AsyncSession
from .model import Collection
from .schemas import createCollectionSchema
class CollectionService():
    async def addCollection(db:AsyncSession):
        pass
