from pydantic import BaseModel

class collectionBase(BaseModel):
    name: str
class createCollectionSchema(collectionBase):
    collectionOwner_id:int

class modifyCollectionSchema(BaseModel):
    id: int
    name:str