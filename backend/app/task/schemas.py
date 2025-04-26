from pydantic import BaseModel
from .model import TaskPriority
class TaskBase(BaseModel):
    name:str
    priority:TaskPriority = TaskPriority.NONE
    collection_id:int


class addTaskSchema(TaskBase):
    pass

class updateTaskSchema(BaseModel):
    id:int
    name:str
    priority:TaskPriority = TaskPriority.NONE
    completed:bool = False