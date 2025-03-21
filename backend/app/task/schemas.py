from pydantic import BaseModel
from .model import TaskPriority
from datetime import datetime
class TaskBase(BaseModel):
    name:str
    priority:TaskPriority = TaskPriority.NONE
    completed:bool = False
    completed_date:datetime = None
    collection_id:int

class Task(TaskBase):
    id:int

class addTaskSchema(TaskBase):
    pass

class deleteTaskSchema(BaseModel):
    id: int
    collection_id: int


class updateTaskSchema(TaskBase):
    pass