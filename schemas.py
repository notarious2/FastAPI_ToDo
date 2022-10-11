from datetime import datetime
from pydantic import BaseModel
from typing import Optional



class TaskBase(BaseModel):
    date: datetime
    text: str
    class Config:
        orm_mode = True
class TaskCreate(TaskBase):
    pass

class TaskDisplay(TaskBase):
    user_id: str
    class Config:
        orm_mode = True

class Task(TaskBase):
    task_id: str
    user_id: str
    # class Config:
    #     orm_mode = True




class User(BaseModel):
    user_id: str
    name: str
    email: str
    username: str
    password: str
    # class Config:
    #     orm_mode = True

class UserCreate(BaseModel):
    name: str
    email: str
    username: str
    password: str
    
    class Config:
        orm_mode = True

class UserDisplay(BaseModel):
    username: str
    email: str
    # makes links between User and UserDisplay schemas
    class Config:
        orm_mode = True