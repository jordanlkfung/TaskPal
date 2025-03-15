from typing import List
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id= Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    date_created = Column(DateTime, default =datetime.datetime.now)
    collection = relationship('Collection', back_populates='users')
