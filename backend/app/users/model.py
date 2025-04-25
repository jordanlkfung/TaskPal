from typing import List, TYPE_CHECKING
from sqlalchemy.orm import relationship, mapped_column, Mapped
import datetime
from app.database import Base
if TYPE_CHECKING: #type checking needed to pass flake test
    from app.collection.model import Collection

class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True)
    email:Mapped[str] = mapped_column(unique=True)
    password:Mapped[str]
    date_created:Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    collection:Mapped[List['Collection']] = relationship(back_populates='collectionOwner')

