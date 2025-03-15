from fastapi import APIRouter

collection_router = APIRouter()

@collection_router.get('/{userId}')
async def getUserCollections(userId):
    pass

@collection_router.post("/")
async def addCollection():
    pass

@collection_router.delete("/{collection_id}")
async def deleteCollection(collection_id:int):
    pass

@collection_router.patch("/{collection_id}")
async def modifyCollection(collection_id:int):
    pass