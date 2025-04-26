from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from app.users.model import User
    from app.task.model import Task

class Collection(Base):
    __tablename__ = 'collection'

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]
    collectionOwner_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    collectionOwner:Mapped['User'] = relationship(back_populates='collection')
    task:Mapped[List['Task']] = relationship(back_populates='collection')