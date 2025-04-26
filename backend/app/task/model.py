from datetime import datetime
import enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.collection.model import Collection

class TaskPriority(enum.Enum):
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    NONE = 0

class Task(Base):
    __tablename__ = "task"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]
    priority:Mapped[TaskPriority]
    creation_date:Mapped[datetime] =mapped_column(default=datetime.now)
    completed:Mapped[bool] = mapped_column(default=False)
    collection_id:Mapped[int] = mapped_column(ForeignKey('collection.id'))
    collection:Mapped['Collection'] = relationship(back_populates='task')