from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Collection(Base):
    __tablename__ = 'collection'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    collectionOwner_id = Column(Integer, ForeignKey('users.id'))
    collectionOwner = relationship('User', back_populates='collection')
    task = relationship('Task', back_populates='collection')