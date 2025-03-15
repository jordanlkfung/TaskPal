from .database import Base, engine
from .users import model as user_model
from .task import model as task_model
from .collection import model as collection_model

def create_tables():
    Base.metadata.create_all(bind=engine)
