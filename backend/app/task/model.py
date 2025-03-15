import datetime
import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship

from app.database import Base

class TaskPriority(enum.Enum):
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    NONE = 0

class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.NONE)
    creation_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    completed = Column(Boolean, default=False)
    completed_date = Column(DateTime)
    collection_id = Column(Integer, ForeignKey('collection.id'))
    collection = relationship('Collection', back_populates='task')