from pydantic import BaseModel

class createCollectionSchema(BaseModel):
    name: str
    collectionOwner_id:int
