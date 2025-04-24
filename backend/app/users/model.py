from typing import List, TYPE_CHECKING
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
import datetime
from app.database import Base
if TYPE_CHECKING:
    from app.collection.model import Collection

class User(Base):
    __tablename__ = "users"
    id= Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    date_created = Column(DateTime, default =datetime.datetime.now)
    collection = relationship('Collection', back_populates='collectionOwner')
