from pydantic import BaseModel
from .model import TaskPriority
class TaskBase(BaseModel):
    '''schema used for what is expected in body of requests'''
    name:str
    priority:TaskPriority = TaskPriority.NONE
    collection_id:int


class addTaskSchema(TaskBase):
    '''schema of what is expect in body of POST requests to add tasks'''
    pass

class updateTaskSchema(BaseModel):
    '''schema for what is expect in patch requests'''
    id:int
    name:str
    priority:TaskPriority = TaskPriority.NONE
    completed:bool = False