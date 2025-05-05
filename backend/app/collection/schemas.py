from pydantic import BaseModel

class collectionBase(BaseModel):
    '''schema for body ofrequests to collection endpoint'''
    name: str
class createCollectionSchema(collectionBase):
    '''schema for body of requests to create collection'''
    collectionOwner_id:int

class modifyCollectionSchema(BaseModel):
    '''chema for body of requests to modify collection'''
    id: int
    name:str