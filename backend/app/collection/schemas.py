from pydantic import BaseModel

class createCollectionSchema(BaseModel):
    name: str
    collectionOwner_id:int

class modifyCollectionSchema(BaseModel):
    id: int
    name:str